from __future__ import annotations

from typing import Any


class HeloError(Exception):
    """Base class for all errors raised by this library."""


class APIConnectionError(HeloError):
    """Raised when the request could not reach the API (network error, timeout)."""

    def __init__(self, message: str = "Connection error.") -> None:
        super().__init__(message)


class APITimeoutError(APIConnectionError):
    """Raised when a request times out."""

    def __init__(self, message: str = "Request timed out.") -> None:
        super().__init__(message)


class APIError(HeloError):
    """Raised when the API returns a non-success status code."""

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


class WebhookSignatureError(HeloError):
    """Base class for every reason a webhook signature is rejected.

    Catch this one class when you do not care why a delivery was rejected.
    """


class WebhookSignatureMalformedHeaderError(WebhookSignatureError):
    """The header was not in the documented ``t={timestamp},v{version}={signature}`` form."""


class WebhookSignatureUnsupportedVersionError(WebhookSignatureError):
    """The header carried only signing schemes this SDK does not know how to verify.

    Upgrading the SDK is the fix; see ``SUPPORTED_WEBHOOK_SIGNATURE_VERSIONS``.
    """


class WebhookSignatureTimestampSkewError(WebhookSignatureError):
    """The signature was correctly formed but its timestamp is too far from the current time.

    It may be a replay.
    """


class WebhookSignatureMismatchError(WebhookSignatureError):
    """The signature did not match the body: it was tampered with, or the signing key is wrong."""
