from __future__ import annotations

from typing import Any


class HeloError(Exception):
    """Base class for all errors raised by this library."""


class APIConnectionError(HeloError):
    """Raised when the request could not reach the Helo API (network error, timeout)."""

    def __init__(self, message: str = "Connection error.") -> None:
        super().__init__(message)


class APITimeoutError(APIConnectionError):
    """Raised when a request times out."""

    def __init__(self, message: str = "Request timed out.") -> None:
        super().__init__(message)


class APIError(HeloError):
    """Raised when the Helo API returns a non-success status code."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        error_code: str | None = None,
        detail: str | None = None,
        request_id: str | None = None,
        response_data: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code
        self.detail = detail
        self.request_id = request_id
        self.response_data = response_data


class BadRequestError(APIError):
    pass


class AuthenticationError(APIError):
    pass


class PermissionDeniedError(APIError):
    pass


class NotFoundError(APIError):
    pass


class ConflictError(APIError):
    pass


class UnprocessableEntityError(APIError):
    pass


class RateLimitError(APIError):
    """Raised on HTTP 429. ``retry_after`` is the server-suggested delay in seconds, if any."""

    def __init__(self, message: str, *, retry_after: float | None = None, **kwargs: Any) -> None:
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class InternalServerError(APIError):
    pass
