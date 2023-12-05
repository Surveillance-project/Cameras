from enum import StrEnum
from abc import ABC, abstractmethod
import urllib3
from Cameras.settings import WINDY_KEY, WINDY_PAGINTATION_LIMIT_LIMIT
from bs4 import BeautifulSoup
from helpers.responses import handle_broad_api_error_status as handle_error_status
from .caching import WebcamDataCaching, WindyWebcamImageCaching, WindyWebcamMetaCaching
from custom_exceptions.caching import (EmptyImageCacheException, CameraSchemeNotInCacheException,
                                       MetaIsAbsentInCacheException)
from custom_exceptions.windy_api import NoSuchCameraException, ResponseException
from logging import getLogger


logger = getLogger()


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


class WebcamImageApi(WebcamApi, ABC):
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
        """
        :returns: full webcam schema, meaning that every additional parameter is used (Done with UrlBuilder).
        In order to request only necessary data, use url alternative method.
        """
        url = WindyApi.WebcamSchemeURLBuilder() \
            .add_urls() \
            .add_location() \
            .add_player() \
            .add_images() \
            .add_categories() \
            .create(camera_id)
        response_json = self.get_camera_by_url(url)

        return response_json

    def get_camera_by_url(self, url) -> dict:
        response = WindyApi.__http.request('GET', url)
        try:
            handle_error_status(response.status)
        except ResponseException as e:
            if e.status_code == 404:
                raise NoSuchCameraException()

        return response.json()

    def get_images(self, camera_id: int, period: WebcamLifecyclePeriod) -> list[bytes]:
        camera_schema = self.get_camera(camera_id)
        player_url = self.get_player_url(camera_schema, period)
        player_html = self.get_player_html(player_url)
        images_urls = self.get_player_images_urls(player_html)
        downloaded_images = list()
        for image_url in images_urls:
            image = self.get_image(image_url)
            downloaded_images.append(image)
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
            self.limit_limit = WINDY_PAGINTATION_LIMIT_LIMIT
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

        def add_limit(self, limit: int):
            if type(limit) is not int:
                raise ValueError('Limit should be of int type')
            if not (0 <= limit <= self.limit_limit):
                raise ValueError(f"Limit value needs to be between 0 and {self.limit_limit}")
            self.params.add(f'limit={limit}')

        def add_offset(self, offset: int):
            if type(offset) is not int:
                raise ValueError('Limit should be of int type')
            if offset < 0:
                raise ValueError(f"Limit value needs to be a positive number")
            self.params.add(f'offset={offset}')

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


class WebcamDataManager(ABC):
    """
    Handles data retrieval strategies. Hits api, caches and retrieves the data on demand.
    """
    def __init__(self, api_strategy: WebcamApi, caching_strategy: WebcamDataCaching):
        self._api = api_strategy
        self._caching_strategy = caching_strategy

    @property
    def caching_strategy(self) -> WebcamDataCaching:
        return self._caching_strategy

    @caching_strategy.setter
    def caching_strategy(self, value):
        self._caching_strategy = value

    @property
    def api(self) -> WebcamApi:
        """
        Strategy for hitting api where data is stored.
        """
        return self._api

    @api.setter
    def api(self, value: WebcamApi):
        self._api = value


class WebcamImageManager(WebcamDataManager):
    pass


class WindyWebcamImageManager(WebcamImageManager):
    def __init__(self):
        super().__init__(WindyApi(), WindyWebcamImageCaching())

    @property
    def caching_strategy(self) -> WindyWebcamImageCaching:
        return self._caching_strategy

    @caching_strategy.setter
    def caching_strategy(self, value):
        raise SyntaxError("Assigning is restricted")

    @property
    def api(self) -> WindyApi:
        return self._api

    @api.setter
    def api(self, value):
        raise SyntaxError("Assigning is restricted")

    def get_images(self, camera_id: int) -> list[bytes]:
        """
        :raises NoSuchCameraException: if attempted hitting api with not existing camera id
        """
        try:
            images = self.caching_strategy.read(camera_id)
        except (EmptyImageCacheException, CameraSchemeNotInCacheException) as e:
            logger.info(e.message)
            logger.info("Manager tried to retrieve images from cache, but none were found. Trying to hit api")
            images = self.api.get_images(camera_id, WebcamLifecyclePeriod.DAY)
            logger.info("Successfully downloaded images from api")
            self.caching_strategy.cache(images, camera_id)
            logger.info("Successfully cached downloaded images")
        return images


class WindyDataManager(WebcamDataManager):

    @property
    def caching_strategy(self) -> WindyWebcamMetaCaching:
        return self._caching_strategy

    @caching_strategy.setter
    def caching_strategy(self, value):
        raise SyntaxError("Assigning is restricted")

    @property
    def api(self) -> WindyApi:
        return self._api

    @api.setter
    def api(self, value):
        raise SyntaxError("Assigning is restricted")

    def __init__(self):
        super().__init__(WindyApi(), WindyWebcamMetaCaching())
        self._image_caching_manager = WindyWebcamImageManager()

    @property
    def image_caching_manager(self) -> WindyWebcamImageManager:
        return self._image_caching_manager

    # Makes 3 retrieval calls to cache
    def get_data(self, camera_id: int) -> dict:
        """
        :returns: scheme of meta info and images
        :raises NoSuchCameraException: if attempted hitting api with not existing camera id
        """
        try:
            self._image_caching_manager.get_images(camera_id)
            self.caching_strategy.read(camera_id)
        except MetaIsAbsentInCacheException as e:
            logger.info(e.message)
            logger.info("Manager tried to retrieve camera meta from cache, but none was found. Trying to hit api")
            meta = self.api.get_camera(camera_id)
            logger.info("Successfully downloaded camera meta from api")
            self.caching_strategy.cache(meta, camera_id)
            logger.info("Successfully cached downloaded camera meta")

        return self.caching_strategy.read_schema(camera_id)

