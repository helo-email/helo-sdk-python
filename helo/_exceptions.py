from __future__ import annotations

from typing import Any, Optional


class HeloError(Exception):
    pass


class APIError(HeloError):
    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        error_code: Optional[str] = None,
        detail: Optional[str] = None,
        request_id: Optional[str] = None,
        response_data: Optional[dict[str, Any]] = None,
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


class UnprocessableEntityError(APIError):
    pass


class InternalServerError(APIError):
    pass
