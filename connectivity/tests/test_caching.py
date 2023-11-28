from django.test.testcases import TestCase
from services.caching import WindyWebcamImageCaching
from django.core.cache import cache


class WriteImagesToRedisTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.caching_strategy = WindyWebcamImageCaching()
        cls.webcam_id = 1179853135

    def tearDown(self):
        cache.clear()

    def test_write_fakes(self):
        fake_images = [b'0', b'1']
        self.__class__.caching_strategy.cache(fake_images, self.__class__.webcam_id)
        webcam_scheme = cache.get(str(self.__class__.webcam_id))
        self.assertEquals(webcam_scheme["images"]["raw"], fake_images)

    def test_write_fake(self):
        fake_image = [b'0']
        self.__class__.caching_strategy.cache(fake_image, self.__class__.webcam_id)
        webcam_scheme = cache.get(str(self.__class__.webcam_id))
        self.assertEquals(webcam_scheme["images"]["raw"], fake_image)
