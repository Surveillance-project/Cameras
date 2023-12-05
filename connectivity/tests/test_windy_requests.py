"""
To be noticed: these tests are mostly api calls and will take a lot of time, if ran
"""

from unittest.case import TestCase as UnitCase
from services.connectivity import WindyApi, WebcamLifecyclePeriod
from .big_constants import WINDY_PLAYER_HTML
from custom_exceptions.windy_api import NoSuchCameraException


class AuthorizesTest(UnitCase):
    def setUp(self):
        self.api = WindyApi()

    def test_authorization(self):
        self.api.authorize()


class GetWebcamSchemeTest(UnitCase):
    def setUp(self):
        self.webcam_id = 1179853135
        self.api = WindyApi()

    def test_get_full_scheme(self):
        self.api.get_camera(self.webcam_id)

    def test_get_scheme_with_invalid_id_raises_exception(self):
        self.assertRaises(NoSuchCameraException, self.api.get_camera, -1)

    def test_get_partial_scheme_with_url(self):
        self.api.get_camera_by_url(WindyApi.WebcamSchemeURLBuilder()
                                   .add_images()
                                   .create(self.webcam_id))


class GetPlayerUrlTest(UnitCase):

    def setUp(self):
        self.api = WindyApi()
        self.webcam_scheme = {
            "title": "Sydney: Sydney Harbour Bridge - Sydney Opera House",
            "viewCount": 1387607,
            "webcamId": 1179853135,
            "status": "active",
            "lastUpdatedOn": "2023-11-26T13:29:36.000Z",
            "player": {
                "live": "https://webcams.windy.com/webcams/public/embed/player/1179853135/live",
                "day": "https://webcams.windy.com/webcams/public/embed/player/1179853135/day",
                "month": "https://webcams.windy.com/webcams/public/embed/player/1179853135/month",
                "year": "https://webcams.windy.com/webcams/public/embed/player/1179853135/year",
                "lifetime": "https://webcams.windy.com/webcams/public/embed/player/1179853135/lifetime"
            }
        }

    def test_get_player_for_day_url(self):
        self.api.get_player_url(self.webcam_scheme)

    def test_get_player_for_live_url(self):
        self.api.get_player_url(self.webcam_scheme, WebcamLifecyclePeriod.LIVE)

    def test_get_player_for_month_url(self):
        self.api.get_player_url(self.webcam_scheme, WebcamLifecyclePeriod.MONTH)

    def test_get_player_for_year_url(self):
        self.api.get_player_url(self.webcam_scheme, WebcamLifecyclePeriod.YEAR)


class GetPlayerHTMLTest(UnitCase):

    def setUp(self):
        self.api = WindyApi()
        self.player_for_day_url = "https://webcams.windy.com/webcams/public/embed/player/1179853135/day"

    def test_return_html(self):
        html_string = self.api.get_player_html(self.player_for_day_url)
        self.assertTrue(html_string.strip().strip('\n').startswith("<!doctype html>"))


class GetPlayerImagesUrlsTest(UnitCase):
    def setUp(self):
        self.api = WindyApi()
        self.html = WINDY_PLAYER_HTML

    def test_get_images_urls(self):
        urls = self.api.get_player_images_urls(self.html)
        self.assertIsInstance(urls, list)


class GetImagesPipelineTest(UnitCase):
    def setUp(self):
        self.webcam_id = 1179853135
        self.api = WindyApi()

    def test_download_images(self):
        images = self.api.get_images(self.webcam_id, WebcamLifecyclePeriod.DAY)
        self.assertIsNot(bool(images), False)
