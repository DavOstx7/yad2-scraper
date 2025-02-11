import httpx
from typing import List


class ResponseError(httpx.HTTPStatusError):
    # This adds the request/response objects to the error
    pass


class AntiBotDetectedError(ResponseError):
    pass


class UnexpectedContentError(ResponseError):
    pass


class MaxRetriesExceededError(Exception):
    def __init__(self, msg: str, errors: List[Exception] = None):
        super().__init__(msg)
        self.errors = errors


class MaxRequestRetriesExceededError(MaxRetriesExceededError):
    def __init__(self, method: str, url: str, max_retries: int, errors: List[Exception] = None):
        self.method = method
        self.url = url
        self.max_retries = max_retries

        msg = f"All {self.max_retries} retry attempts for {self.method} request to '{self.url}' have failed"
        super().__init__(msg, errors)
