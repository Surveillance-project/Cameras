from abc import ABC, abstractmethod
from django.core.cache import cache
from custom_exceptions.caching import EmptyImageCacheException, CameraSchemeNotInCacheException


class WebcamDataCaching(ABC):
    @abstractmethod
    def read(self, camera_id):
        raise NotImplementedError()

    @abstractmethod
    def cache(self, images: list[bytes], camera_id):
        raise NotImplementedError()


class WebcamImageCaching(WebcamDataCaching, ABC):

    @abstractmethod
    def cache(self, images: list[bytes], camera_id):
        raise NotImplementedError()


class WindyWebcamImageCaching(WebcamImageCaching):
    IMAGES_REFRESH_RATE = 60 * 10

    def read(self, camera_id) -> dict:
        webcam_scheme = cache.get(str(camera_id))
        if webcam_scheme:
            return webcam_scheme
        else:
            raise CameraSchemeNotInCacheException(f"Camera (id: {camera_id}) scheme is absent in cache")

    """
    :raises EmptyImageCacheException: if there are now images stored
    """
    def read_images(self, camera_id) -> list[bytes]:
        webcam_scheme = self.read(camera_id)
        images: list[bytes] = webcam_scheme["images"]["raw"]
        if images:
            return images
        raise EmptyImageCacheException

    def cache(self, images: list[bytes], camera_id: int):
        camera_scheme = cache.get(str(camera_id))
        if camera_scheme:
            if "images" in camera_scheme.keys():
                camera_scheme["images"]["raw"] = images
            else:
                camera_scheme["images"] = {"raw": images}
        else:
            cache.set(str(camera_id), {
                "images": {"raw": images}
            }, timeout=WindyWebcamImageCaching.IMAGES_REFRESH_RATE)
