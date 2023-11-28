class ResponseException(Exception):
    def __init__(self, status_code: int, message='', errors=[]):
        super().__init__(message)
        self.status_code = status_code
        self.message = message
        self.errors = errors


class AuthorizationException(ResponseException):
    STATUS_CODE = 401

    def __init__(self, message='Authorization failed', errors=[]):
        super().__init__(self.__class__.STATUS_CODE, message, errors)


class NoSuchCameraException(ResponseException):
    STATUS_CODE = 404

    def __init__(self, message=None, camera_id=None, errors=[]):
        self.camera_id = camera_id
        if not message:
            if camera_id:
                message = f"Camera with id: {self.camera_id} does not exist"
            else:
                message = "Camera with such id does not exist"
        super().__init__(self.__class__.STATUS_CODE, message, errors)
