from __future__ import annotations

from pytest_httpx import HTTPXMock

import sdk_helo_email as helo


def test_list(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        json={
            "totalCount": 1,
            "results": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "createdAt": "2024-01-01T00:00:00Z",
                    "name": "example",
                    "verified": True,
                }
            ],
        },
    )

    client.domains.list()

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "GET"
    assert request.url.path == "/domains"


def test_create(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        json={
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "createdAt": "2024-01-01T00:00:00Z",
            "name": "example",
            "verified": True,
            "dnsRecords": {},
        },
    )

    client.domains.create(
        name="test-name",
        channel_ids=["550e8400-e29b-41d4-a716-446655440000"],
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "POST"
    assert request.url.path == "/domains"


def test_retrieve(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        json={
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "createdAt": "2024-01-01T00:00:00Z",
            "name": "example",
            "verified": True,
            "dnsRecords": {},
        },
    )

    client.domains.retrieve(
        "550e8400-e29b-41d4-a716-446655440000",
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "GET"
    assert request.url.path == "/domains/550e8400-e29b-41d4-a716-446655440000"


def test_update(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="PATCH",
        json={
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "createdAt": "2024-01-01T00:00:00Z",
            "name": "example",
            "verified": True,
        },
    )

    client.domains.update(
        "550e8400-e29b-41d4-a716-446655440000",
        channel_ids=["550e8400-e29b-41d4-a716-446655440000"],
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "PATCH"
    assert request.url.path == "/domains/550e8400-e29b-41d4-a716-446655440000"


def test_delete(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="DELETE",
        status_code=204,
    )

    client.domains.delete(
        "550e8400-e29b-41d4-a716-446655440000",
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "DELETE"
    assert request.url.path == "/domains/550e8400-e29b-41d4-a716-446655440000"


def test_verify(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        json={},
    )

    client.domains.verify(
        "550e8400-e29b-41d4-a716-446655440000",
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "POST"
    assert request.url.path == "/domains/550e8400-e29b-41d4-a716-446655440000/verify"


def test_rotate_key(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        json={},
    )

    client.domains.rotate_key(
        "550e8400-e29b-41d4-a716-446655440000",
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "POST"
    assert request.url.path == "/domains/550e8400-e29b-41d4-a716-446655440000/rotate-key"


async def test_list_async(async_client: helo.AsyncHelo, httpx_mock: HTTPXMock) -> None:
    """The async resource is generated from the same operation, so one call proves the pair."""
    httpx_mock.add_response(
        method="GET",
        json={
            "totalCount": 1,
            "results": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "createdAt": "2024-01-01T00:00:00Z",
                    "name": "example",
                    "verified": True,
                }
            ],
        },
    )

    await async_client.domains.list()

    request = httpx_mock.get_request()
    assert request is not None
    assert request.url.path == "/domains"
