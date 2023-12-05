class CacheException(Exception):
    def __init__(self, message, errors=[]):
        super().__init__(message)
        self.message = message
        self.errors = errors


class EmptyImageCacheException(CacheException):
    def __init__(self, message="Images are absent in cache of the camera", errors=[]):
        super().__init__(message, errors)


class MetaIsAbsentInCacheException(CacheException):
    pass


class CameraSchemeNotInCacheException(CacheException):
    def __init__(self, message="Camera schema is absent in cache", errors=[]):
        super().__init__(message, errors)
