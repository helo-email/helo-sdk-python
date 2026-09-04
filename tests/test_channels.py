from __future__ import annotations

from pytest_httpx import HTTPXMock

import sdk_helo_email as helo


def test_list(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        json={"results": [{}], "totalCount": 1},
    )

    client.channels.list()

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "GET"
    assert request.url.path == "/channels"


def test_create(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        json={},
    )

    client.channels.create(
        name="test-name",
        delivery_type=helo.DeliveryType.LIVE,
        tracking={"links": True, "opens": True},
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "POST"
    assert request.url.path == "/channels"


def test_retrieve(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        json={},
    )

    client.channels.retrieve(
        "550e8400-e29b-41d4-a716-446655440000",
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "GET"
    assert request.url.path == "/channels/550e8400-e29b-41d4-a716-446655440000"


def test_update(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="PATCH",
        json={},
    )

    client.channels.update(
        "550e8400-e29b-41d4-a716-446655440000",
        name="test-name",
        delivery_type=helo.DeliveryType.LIVE,
        tracking={"links": True, "opens": True},
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "PATCH"
    assert request.url.path == "/channels/550e8400-e29b-41d4-a716-446655440000"


def test_delete(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="DELETE",
        status_code=204,
    )

    client.channels.delete(
        "550e8400-e29b-41d4-a716-446655440000",
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "DELETE"
    assert request.url.path == "/channels/550e8400-e29b-41d4-a716-446655440000"


async def test_list_async(async_client: helo.AsyncHelo, httpx_mock: HTTPXMock) -> None:
    """The async resource is generated from the same operation, so one call proves the pair."""
    httpx_mock.add_response(
        method="GET",
        json={"results": [{}], "totalCount": 1},
    )

    await async_client.channels.list()

    request = httpx_mock.get_request()
    assert request is not None
    assert request.url.path == "/channels"
