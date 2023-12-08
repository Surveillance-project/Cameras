import base64
from abc import ABC, abstractmethod
from django.core.cache import cache
from custom_exceptions.caching import EmptyImageCacheException, CameraSchemeNotInCacheException, MetaIsAbsentInCacheException


class WebcamDataCaching(ABC):
    def read_schema(self, camera_id):
        webcam_scheme = cache.get(str(camera_id))
        if webcam_scheme:
            return webcam_scheme
        else:
            raise CameraSchemeNotInCacheException(f"Camera (id: {camera_id}) scheme is absent in cache")

    @abstractmethod
    def read(self, camera_id):
        raise NotImplementedError()

    @abstractmethod
    def cache(self, camera_id):
        raise NotImplementedError()


class WebcamImageCaching(WebcamDataCaching, ABC):

    @abstractmethod
    def cache(self, images: list[bytes], camera_id):
        raise NotImplementedError()


class WindyWebcamImageCaching(WebcamImageCaching):
    IMAGES_REFRESH_RATE = 60 * 10

    def __init__(self, with_base64: bool = False):
        self.with_base64 = with_base64

    """
    :raises EmptyImageCacheException: if there are now images stored
    :raises KeyError: if the scheme exists without demanded values for storing images
    """
    def read(self, camera_id) -> list[bytes]:
        webcam_scheme = self.read_schema(camera_id)
        try:
            images: list[bytes] = webcam_scheme["images"]["raw"]
            return images
        except KeyError as e:
            raise EmptyImageCacheException(errors=[e])

    def cache(self, images: list[bytes], camera_id: int):
        if self.with_base64:
            images_base64 = []
            for image in images:
                image_base64 = base64.b64encode(image)
                images_base64.append(image_base64)
            images = images_base64
        try:
            camera_scheme = self.read_schema(camera_id)
        except CameraSchemeNotInCacheException as e:
            camera_scheme = dict()
        finally:
            if "images" in camera_scheme.keys():
                camera_scheme["images"]["raw"] = images
            else:
                camera_scheme["images"] = {"raw": images}

        cache.set(str(camera_id), camera_scheme,
                  timeout=WindyWebcamImageCaching.IMAGES_REFRESH_RATE)


class WindyWebcamMetaCaching(WebcamDataCaching):

    def read(self, camera_id) -> dict:
        webcam_scheme = self.read_schema(camera_id)
        try:
            meta: dict = webcam_scheme["meta"]
            return meta
        except KeyError as e:
            raise MetaIsAbsentInCacheException("Meta is not found", [e])

    def cache(self, meta: dict, camera_id):
        try:
            camera_scheme = self.read_schema(camera_id)
        except CameraSchemeNotInCacheException as e:
            camera_scheme = dict()
        finally:
            camera_scheme["meta"] = meta
        cache.set(str(camera_id), camera_scheme,
                  timeout=WindyWebcamImageCaching.IMAGES_REFRESH_RATE)
