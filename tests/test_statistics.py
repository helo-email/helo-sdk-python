from __future__ import annotations

from pytest_httpx import HTTPXMock

import sdk_helo_email as helo


def test_retrieve_hourly(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        json={},
    )

    client.statistics.retrieve_hourly(
        from_="2024-01-01T00:00:00Z",
        to="2024-01-01T00:00:00Z",
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "GET"
    assert request.url.path == "/statistics/hourly"


def test_retrieve_daily(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        json={},
    )

    client.statistics.retrieve_daily(
        from_="2024-01-01",
        to="2024-01-01",
        timezone="America/New_York",
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "GET"
    assert request.url.path == "/statistics/daily"


def test_retrieve_totals(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        json={},
    )

    client.statistics.retrieve_totals(
        from_="2024-01-01T00:00:00Z",
        to="2024-01-01T00:00:00Z",
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "GET"
    assert request.url.path == "/statistics/totals"


async def test_retrieve_hourly_async(async_client: helo.AsyncHelo, httpx_mock: HTTPXMock) -> None:
    """The async resource is generated from the same operation, so one call proves the pair."""
    httpx_mock.add_response(
        method="GET",
        json={},
    )

    await async_client.statistics.retrieve_hourly(
        from_="2024-01-01T00:00:00Z",
        to="2024-01-01T00:00:00Z",
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.url.path == "/statistics/hourly"
