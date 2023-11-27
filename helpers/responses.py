from custom_exceptions.windy_api import ResponseException, AuthorizationException


def handle_broad_api_error_status(status):
    if status == 401:
        raise AuthorizationException('Authorization failed')
    elif status >= 400:
        raise ResponseException('Client side error')
    elif status >= 500:
        raise ResponseException('Server side error')
