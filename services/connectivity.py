from enum import StrEnum

import urllib3
from Cameras.settings import WINDY_KEY
from custom_exceptions.windy_api import ResponseException, AuthorizationException
from bs4 import BeautifulSoup

WINDY_API_URL = 'https://api.windy.com'
__http = urllib3.PoolManager(headers={'X-WINDY-API-KEY': WINDY_KEY})


class WebcamLifecyclePeriod(StrEnum):
    LIVE = 'live'
    DAY = 'day'
    MONTH = 'month'
    YEAR = 'year'
    LIFETIME = 'lifetime'


def authorize():
    response = __http.request('GET', WINDY_API_URL + '/webcams/api/v3/webcams')
    if response.status == 401:
        raise AuthorizationException('Authorization failed')
    elif response.status >= 400:
        raise ResponseException('Client side error')
    elif response.status >= 500:
        raise ResponseException('Server side error')


def get_full_webcam_schema(webcam_id):
    url = WebcamSchemeURLBuilder() \
        .add_urls() \
        .add_location() \
        .add_player() \
        .add_images() \
        .add_categories() \
        .create(webcam_id)
    response = __http.request('GET', url)
    if response.status == 401:
        raise AuthorizationException('Authorization failed')
    elif response.status >= 400:
        raise ResponseException('Client side error')
    elif response.status >= 500:
        raise ResponseException('Server side error')

    return response.json()


def get_player_url(webcam_scheme: dict, time_period: WebcamLifecyclePeriod = WebcamLifecyclePeriod.DAY):
    return webcam_scheme["player"][time_period.value]


def get_player_html(url: str) -> str:
    response = __http.request('GET', url)
    if response.status == 401:
        raise AuthorizationException('Authorization failed')
    elif response.status >= 400:
        raise ResponseException('Client side error')
    elif response.status >= 500:
        raise ResponseException('Server side error')
    return response.data.decode('utf-8')


def get_player_images_urls(html: str) -> list[str]:
    parsed_html = BeautifulSoup(html)
    raw_urls_str = parsed_html.find('script').text.split('full: [')[1].split(']')[0]
    raw_urls_phase1 = raw_urls_str.split("'")  # ['', '\'url\'', ', ' 'url', ', ', 'url', '']
    urls = []
    step = 2  # urls are always at odd indexes
    first_url_index = 1
    for i in range(first_url_index, len(raw_urls_phase1), step):
        urls.append(raw_urls_phase1[i].strip("'"))
    return urls


def get_image(url: str) -> bytes:
    response = __http.request('GET', url)
    if response.status == 401:
        raise AuthorizationException('Authorization failed')
    elif response.status >= 400:
        raise ResponseException('Client side error')
    elif response.status >= 500:
        raise ResponseException('Server side error')
    return response.data


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
