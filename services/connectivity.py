import urllib3
from Cameras.settings import WINDY_KEY
from custom_exceptions.windy_api import ResponseException, AuthorizationException


WINDY_API_URL = 'https://api.windy.com'


__http = urllib3.PoolManager(headers={'X-WINDY-API-KEY': WINDY_KEY})


def authorize():
    response = __http.request('GET', WINDY_API_URL+'/webcams/api/v3/webcams')
    if response.status == 200:
        return
    elif response.status == 401:
        raise AuthorizationException('Authorization failed')
    elif response.status >= 400:
        raise ResponseException('Client side error')
    elif response.status >= 500:
        raise ResponseException('Server side error')


def get_full_webcam_schema(webcam_id):
    url = WebcamSchemeURLBuilder()\
        .add_urls()\
        .add_location()\
        .add_player()\
        .add_images()\
        .add_categories()\
        .create(webcam_id)
    response = __http.request('GET', url)
    return response.json()


class WebcamSchemeURLBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self.__url = WINDY_API_URL + '/webcams/api/v3/webcams/{webcam_id}?include='
        self.__parametrized = False
        self.params = set()

    def create(self, webcam_id):
        if not self.__parametrized:
            self.__url += ','.join(self.params)
            self.__parametrized = True
        return self.__url.format(webcam_id=webcam_id)

    def add_categories(self):
        self.params.add('categories')
        return self

    def add_images(self):
        self.params.add('images')
        return self

    def add_location(self):
        self.params.add('location')
        return self

    def add_player(self):
        self.params.add('player')
        return self

    def add_urls(self):
        self.params.add('urls')
        return self
