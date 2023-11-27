from enum import StrEnum
from abc import ABC, abstractmethod
import urllib3
from Cameras.settings import WINDY_KEY
from bs4 import BeautifulSoup
from helpers.responses import handle_broad_api_error_status as handle_error_status


class WebcamLifecyclePeriod(StrEnum):
    LIVE = 'live'
    DAY = 'day'
    MONTH = 'month'
    YEAR = 'year'
    LIFETIME = 'lifetime'


class WebcamApi(ABC):
    @abstractmethod
    def authorize(self):
        pass

    @abstractmethod
    def get_camera(self, camera_id):
        pass


class WebcamImageApi(WebcamApi):
    @abstractmethod
    def get_images(self, camera_id, period):
        pass


class WindyApi(WebcamImageApi):
    URL = 'https://api.windy.com'
    __http = urllib3.PoolManager(headers={'X-WINDY-API-KEY': WINDY_KEY})

    def authorize(self):
        response = WindyApi.__http.request('GET', WindyApi.URL + '/webcams/api/v3/webcams')
        handle_error_status(response.status)

    def get_camera(self, camera_id) -> dict:
        url = WindyApi.WebcamSchemeURLBuilder() \
            .add_urls() \
            .add_location() \
            .add_player() \
            .add_images() \
            .add_categories() \
            .create(camera_id)
        response = WindyApi.__http.request('GET', url)
        handle_error_status(response.status)

        return response.json()

    def get_images(self, camera_id: int, period: WebcamLifecyclePeriod) -> list[bytes]:
        camera_schema = self.get_camera(camera_id)
        player_url = self.get_player_url(camera_schema, period)
        player_html = self.get_player_html(player_url)
        images_urls = self.get_player_images_urls(player_html)
        downloaded_images = set()
        for image_url in images_urls:
            image = self.get_image(image_url)
            downloaded_images.add(image)
        return downloaded_images

    def get_player_url(self, webcam_scheme: dict, time_period: WebcamLifecyclePeriod = WebcamLifecyclePeriod.DAY):
        return webcam_scheme["player"][time_period.value]

    def get_player_html(self, url: str) -> str:
        response = WindyApi.__http.request('GET', url)
        handle_error_status(response.status)
        return response.data.decode('utf-8')

    def get_player_images_urls(self, html: str) -> list[str]:
        parsed_html = BeautifulSoup(html, features='html.parser')
        raw_urls_str = parsed_html.find('script').text.split('full: [')[1].split(']')[0]
        raw_urls_phase1 = raw_urls_str.split("'")  # ['', '\'url\'', ', ' 'url', ', ', 'url', '']
        urls = []
        step = 2  # urls are always at odd indexes
        first_url_index = 1
        for i in range(first_url_index, len(raw_urls_phase1), step):
            urls.append(raw_urls_phase1[i].strip("'"))
        return urls

    def get_image(self, url: str) -> bytes:
        response = WindyApi.__http.request('GET', url)
        handle_error_status(response.status)
        return response.data

    class WebcamSchemeURLBuilder:
        def __init__(self):
            self.reset()

        def reset(self):
            self.__url = WindyApi.URL + '/webcams/api/v3/webcams/{webcam_id}?include='
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
