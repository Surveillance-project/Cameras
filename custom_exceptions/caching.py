class EmptyImageCacheException(Exception):
    def __init__(self, message="Images are absent in cache of the camera", errors=[]):
        super().__init__(message)
        self.message = message
        self.errors = errors


class CameraSchemeNotInCacheException(Exception):
    def __init__(self, message="Camera scheme is absent in cache", errors=[]):
        super().__init__(message)
        self.message = message
        self.errors = errors
