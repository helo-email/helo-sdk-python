from __future__ import annotations

import pytest
from pytest_httpx import HTTPXMock

import sdk_helo_email as helo

BASE_URL = "https://api.example.test"


@pytest.fixture
def client(httpx_mock: HTTPXMock) -> helo.Helo:
    """A client whose HTTP calls are intercepted, so no server is needed."""
    return helo.Helo(api_key="test-key", base_url=BASE_URL)


@pytest.fixture
def async_client(httpx_mock: HTTPXMock) -> helo.AsyncHelo:
    return helo.AsyncHelo(api_key="test-key", base_url=BASE_URL)
