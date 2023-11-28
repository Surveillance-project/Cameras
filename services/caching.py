from abc import ABC, abstractmethod
from services.connectivity import WebcamApi, WebcamImageApi, WindyApi
from django.core.cache import cache


class WebcamDataCaching(ABC):
    pass


class WebcamImageCaching(WebcamDataCaching, ABC):

    @abstractmethod
    def cache(self, images: list[bytes], camera_id):
        raise NotImplementedError()


class WindyWebcamImageCaching(WebcamImageCaching):
    IMAGES_REFRESH_RATE = 60 * 10

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
