class ResponseException(Exception):
    def __init__(self, message='', errors=[]):
        super().__init__(message)
        self.message = message
        self.errors = errors


class AuthorizationException(ResponseException):

    def __init__(self, message='Authorization failed', errors=[]):
        super().__init__(message, errors)

