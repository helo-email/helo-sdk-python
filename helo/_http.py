from __future__ import annotations

from typing import Any, Optional

import httpx

from ._exceptions import (
    APIError,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    UnprocessableEntityError,
)
from ._version import __version__

DEFAULT_BASE_URL = "https://api.helohq.com"
DEFAULT_TIMEOUT = 30.0

_STATUS_TO_ERROR: dict[int, type[APIError]] = {
    400: BadRequestError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    422: UnprocessableEntityError,
    500: InternalServerError,
}


class HttpClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self._client = httpx.Client(
            base_url=base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "User-Agent": f"helo-python/{__version__}",
            },
            timeout=timeout,
        )

    def get(
        self,
        path: str,
        *,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Any:
        response = self._client.get(path, params=params, headers=headers)
        return self._handle_response(response)

    def post(
        self,
        path: str,
        *,
        json: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Any:
        response = self._client.post(path, json=json, params=params, headers=headers)
        return self._handle_response(response)

    def patch(
        self,
        path: str,
        *,
        json: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Any:
        response = self._client.patch(path, json=json, headers=headers)
        return self._handle_response(response)

    def delete(
        self,
        path: str,
        *,
        headers: Optional[dict[str, str]] = None,
    ) -> None:
        response = self._client.delete(path, headers=headers)
        self._handle_response(response)

    def _handle_response(self, response: httpx.Response) -> Any:
        if response.status_code == 204:
            return None
        if not response.is_success:
            self._raise_api_error(response)
        if response.content:
            return response.json()
        return None

    def _raise_api_error(self, response: httpx.Response) -> None:
        try:
            data: dict[str, Any] = response.json()
        except Exception:
            data = {}

        message = data.get("title") or data.get("detail") or f"HTTP {response.status_code}"
        cls = _STATUS_TO_ERROR.get(response.status_code, APIError)
        raise cls(
            str(message),
            status_code=response.status_code,
            error_code=data.get("code"),
            detail=data.get("detail"),
            request_id=data.get("requestId"),
            response_data=data,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "HttpClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
