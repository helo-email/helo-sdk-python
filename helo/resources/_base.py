from __future__ import annotations

from .._http import HttpClient


class BaseResource:
    def __init__(self, client: HttpClient) -> None:
        self._http = client
