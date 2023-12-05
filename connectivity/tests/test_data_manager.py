from django.test.testcases import TestCase
from services.connectivity import WindyDataManager
from django.core.cache import cache


class DataManagerRetrieveTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.webcam_id = 1179853135
        cls.manager = WindyDataManager()

    def tearDown(self):
        cache.clear()

    def test_retrieve_data(self):
        schema = self.__class__.manager.get_data(self.__class__.webcam_id)
        self.assertTrue(bool(schema["meta"]["webcamId"]))
        self.assertTrue(bool(schema["meta"]["location"]))
        self.assertIs(type(schema["images"]["raw"][0]), bytes)
