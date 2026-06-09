from __future__ import annotations

import asyncio
import email.utils
import random
import time
from typing import Any

import httpx

from ._exceptions import (
    APIConnectionError,
    APIError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    UnprocessableEntityError,
)
from ._version import __version__

DEFAULT_BASE_URL = "https://api.helohq.com"
DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 2

_INITIAL_RETRY_DELAY = 0.5
_MAX_RETRY_DELAY = 8.0

_STATUS_TO_ERROR: dict[int, type[APIError]] = {
    400: BadRequestError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    409: ConflictError,
    422: UnprocessableEntityError,
    429: RateLimitError,
    500: InternalServerError,
}

# Status codes worth retrying: rate limiting and transient server/gateway errors.
_RETRY_STATUS = frozenset({408, 429, 500, 502, 503, 504})


def _default_headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "User-Agent": f"helo-python/{__version__}",
        "Content-Type": "application/json"
    }


def _error_class(status_code: int) -> type[APIError]:
    if status_code in _STATUS_TO_ERROR:
        return _STATUS_TO_ERROR[status_code]
    if 500 <= status_code < 600:
        return InternalServerError
    return APIError


def _parse_retry_after(response: httpx.Response) -> float | None:
    value = response.headers.get("retry-after")
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        pass
    parsed = email.utils.parsedate_to_datetime(value)
    if parsed is None:
        return None
    delay = parsed.timestamp() - time.time()
    return delay if delay > 0 else None


def _backoff_delay(attempt: int, retry_after: float | None) -> float:
    if retry_after is not None:
        return min(retry_after, _MAX_RETRY_DELAY)
    # Exponential backoff with full jitter.
    base = min(_MAX_RETRY_DELAY, _INITIAL_RETRY_DELAY * (2**attempt))
    return random.uniform(0, base)


def _raise_api_error(response: httpx.Response) -> None:
    try:
        data: dict[str, Any] = response.json()
    except Exception:
        data = {}

    validation_error_str = None
    validation_errors = data.get("errors")
    if validation_errors and len(validation_errors) > 0:
        validation_error_str = ", ".join(f"{key}: {value[0]['message']}" for key, value in validation_errors.items())
    message = validation_error_str or data.get("detail") or data.get("title") or f"HTTP {response.status_code}"
    cls = _error_class(response.status_code)
    kwargs: dict[str, Any] = dict(
        status_code=response.status_code,
        error_code=data.get("code"),
        detail=data.get("detail"),
        request_id=data.get("requestId"),
        response_data=data,
    )
    if cls is RateLimitError:
        raise RateLimitError(str(message), retry_after=_parse_retry_after(response), **kwargs)
    raise cls(str(message), **kwargs)


def _handle_response(response: httpx.Response) -> Any:
    if response.status_code == 204:
        return None
    if not response.is_success:
        _raise_api_error(response)
    if response.content:
        return response.json()
    return None


class HttpClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        self._max_retries = max_retries
        self._client = httpx.Client(
            base_url=base_url,
            headers=_default_headers(api_key),
            timeout=timeout,
        )

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        for attempt in range(self._max_retries + 1):
            try:
                response = self._client.request(
                    method, path, params=params, json=json, headers=headers
                )
            except httpx.TimeoutException as exc:
                if attempt < self._max_retries:
                    time.sleep(_backoff_delay(attempt, None))
                    continue
                raise APITimeoutError() from exc
            except httpx.TransportError as exc:
                if attempt < self._max_retries:
                    time.sleep(_backoff_delay(attempt, None))
                    continue
                raise APIConnectionError() from exc

            if response.status_code in _RETRY_STATUS and attempt < self._max_retries:
                time.sleep(_backoff_delay(attempt, _parse_retry_after(response)))
                continue
            return _handle_response(response)

        raise AssertionError("unreachable")  # pragma: no cover

    def get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return self._request("GET", path, params=params, headers=headers)

    def post(
        self,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return self._request("POST", path, json=json, params=params, headers=headers)

    def patch(
        self,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return self._request("PATCH", path, json=json, headers=headers)

    def delete(
        self,
        path: str,
        *,
        headers: dict[str, str] | None = None,
    ) -> None:
        self._request("DELETE", path, headers=headers)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> HttpClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncHttpClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        self._max_retries = max_retries
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers=_default_headers(api_key),
            timeout=timeout,
        )

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        for attempt in range(self._max_retries + 1):
            try:
                response = await self._client.request(
                    method, path, params=params, json=json, headers=headers
                )
            except httpx.TimeoutException as exc:
                if attempt < self._max_retries:
                    await asyncio.sleep(_backoff_delay(attempt, None))
                    continue
                raise APITimeoutError() from exc
            except httpx.TransportError as exc:
                if attempt < self._max_retries:
                    await asyncio.sleep(_backoff_delay(attempt, None))
                    continue
                raise APIConnectionError() from exc

            if response.status_code in _RETRY_STATUS and attempt < self._max_retries:
                await asyncio.sleep(_backoff_delay(attempt, _parse_retry_after(response)))
                continue
            return _handle_response(response)

        raise AssertionError("unreachable")  # pragma: no cover

    async def get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return await self._request("GET", path, params=params, headers=headers)

    async def post(
        self,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return await self._request("POST", path, json=json, params=params, headers=headers)

    async def patch(
        self,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return await self._request("PATCH", path, json=json, headers=headers)

    async def delete(
        self,
        path: str,
        *,
        headers: dict[str, str] | None = None,
    ) -> None:
        await self._request("DELETE", path, headers=headers)

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> AsyncHttpClient:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.aclose()
