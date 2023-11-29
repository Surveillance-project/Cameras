from django.test.testcases import TestCase
from services.caching import WindyWebcamImageCaching, WindyWebcamMetaCaching
from django.core.cache import cache
from .big_constants import WINDY_WEBCAM_FULL_SCHEME
from custom_exceptions.caching import (CameraSchemeNotInCacheException, MetaIsAbsentInCacheException,
                                       EmptyImageCacheException)


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
        images = self.__class__.caching_strategy.read(self.__class__.webcam_id)
        self.assertEquals(images, fake_images)

    def test_write_fake(self):
        fake_image = [b'0']
        self.__class__.caching_strategy.cache(fake_image, self.__class__.webcam_id)
        images = self.__class__.caching_strategy.read(self.__class__.webcam_id)
        self.assertEquals(images, fake_image)

    def test_read_meta_with_invalid_id_raises_exception(self):
        self.assertRaises(CameraSchemeNotInCacheException, self.__class__.caching_strategy.read,
                          self.__class__.webcam_id)

    def test_read_images_before_cached(self):
        cache.add(str(self.__class__.webcam_id), {'a': 'b'})
        self.assertRaises(EmptyImageCacheException, self.__class__.caching_strategy.read,
                          self.__class__.webcam_id)


class WriteDataToRedisTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.caching_strategy = WindyWebcamMetaCaching()
        cls.webcam_id = 1179853135
        cls.scheme = WINDY_WEBCAM_FULL_SCHEME

    def tearDown(self):
        cache.clear()

    def test_write_meta(self):
        self.__class__.caching_strategy.cache(self.__class__.scheme, self.__class__.webcam_id)
        meta_scheme = self.__class__.caching_strategy.read(self.__class__.webcam_id)
        self.assertEquals(meta_scheme, self.__class__.scheme)

    def test_read_meta_with_invalid_id_raises_exception(self):
        self.assertRaises(CameraSchemeNotInCacheException, self.__class__.caching_strategy.read,
                          self.__class__.webcam_id)

    def test_read_meta_before_cached(self):
        cache.add(str(self.__class__.webcam_id), {'a': 'b'})
        self.assertRaises(MetaIsAbsentInCacheException, self.__class__.caching_strategy.read,
                          self.__class__.webcam_id)
