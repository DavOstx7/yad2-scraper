import httpx
from typing import List, Union


class ResponseError(Exception):
    def __init__(self, msg: str, request: httpx.Request, response: httpx.Response):
        super().__init__(msg)
        self.request = request
        self.response = response


class AntiBotDetectedError(ResponseError):
    pass


class UnexpectedContentError(ResponseError):
    pass


class MaxAttemptsExceededError(Exception):
    def __init__(self, msg: str, max_attempts: int, errors: List[BaseException] = None):
        super().__init__(msg)
        self.max_attempts = max_attempts
        self.errors = errors


class MaxRequestAttemptsExceededError(MaxAttemptsExceededError):
    def __init__(self, method: str, url: str, max_attempts: int, errors: List[Union[httpx.HTTPError, ResponseError]]):
        msg = f"All {max_attempts} attempts for {method} request to '{url}' have failed"
        super().__init__(msg, max_attempts, errors)
        self.method = method
        self.url = url
