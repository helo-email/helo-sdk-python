from __future__ import annotations

from .._http import AsyncHttpClient, HttpClient


class BaseResource:
    def __init__(self, client: HttpClient) -> None:
        self._http = client


class AsyncBaseResource:
    def __init__(self, client: AsyncHttpClient) -> None:
        self._http = client
