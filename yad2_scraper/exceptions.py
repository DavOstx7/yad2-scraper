import httpx
from typing import List, Union


class ResponseError(Exception):
    """Represents an error response from an HTTP request."""

    def __init__(self, msg: str, request: httpx.Request, response: httpx.Response):
        """Initialize with an error message, request, and response objects."""
        super().__init__(msg)
        self.request = request
        self.response = response


class AntiBotDetectedError(ResponseError):
    """Raised when an anti-bot mechanism is detected."""
    pass


class UnexpectedContentError(ResponseError):
    """Raised when the response content is not as expected."""
    pass


class MaxAttemptsExceededError(Exception):
    """Raised when the maximum number of attempts is exceeded."""

    def __init__(self, msg: str, max_attempts: int, errors: List[BaseException] = None):
        """Initialize with an error message, max attempts, and optional errors."""
        super().__init__(msg)
        self.max_attempts = max_attempts
        self.errors = errors


class MaxRequestAttemptsExceededError(MaxAttemptsExceededError):
    """Raised when all HTTP request attempts fail."""

    def __init__(self, method: str, url: str, max_attempts: int, errors: List[Union[httpx.HTTPError, ResponseError]]):
        """Initialize with request method, URL, max attempts, and error list."""
        msg = f"All {max_attempts} attempts for {method} request to '{url}' have failed"
        super().__init__(msg, max_attempts, errors)
        self.method = method
        self.url = url
