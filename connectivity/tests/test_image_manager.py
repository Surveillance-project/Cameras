import base64
from unittest.case import TestCase as UnitCase
from services.connectivity import WindyWebcamImageManager
from django.core.cache import cache


class WindyImageManagerDownloadImages(UnitCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.image_manager = WindyWebcamImageManager()
        cls.webcam_id = 1179853135

    def tearDown(self):
        cache.clear()

    def test_download_images(self):
        image_manager: WindyWebcamImageManager = self.__class__.image_manager
        images = image_manager.get_images(self.__class__.webcam_id)
        self.assertTrue(bool(len(images)))
        self.assertTrue(type(images[0]) is bytes)

    def test_cache_stores_images(self):
        image_manager: WindyWebcamImageManager = self.__class__.image_manager
        downloaded_images = image_manager.get_images(self.__class__.webcam_id)
        # Throws exception if the scheme is invalid or absent
        cached_images = cache.get(str(self.webcam_id))["images"]["raw"]
        self.assertEquals(downloaded_images, cached_images)

    def test_image_is_base64(self):
        image_manager: WindyWebcamImageManager = self.__class__.image_manager
        images = image_manager.get_images(self.__class__.webcam_id)
        self.assertFalse(base64.b64encode(base64.b64decode(images[0])) == images[0])

