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
                    "status": "accepted",
                    "subject": "example",
                    "completion": "example",
                    "messages": 1,
                }
            ],
        },
    )

    client.broadcasts.list(
        channel_id="550e8400-e29b-41d4-a716-446655440000",
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "GET"
    assert request.url.path == "/broadcasts"


def test_retrieve(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        json={
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "createdAt": "2024-01-01T00:00:00Z",
            "status": "accepted",
            "subject": "example",
            "completion": "example",
            "messages": 1,
            "failed": 1,
            "suppressed": 1,
            "content": {},
            "tracking": {"opens": True, "links": True},
            "statistics": {
                "sent": 1,
                "delivered": 1,
                "bounced": 1,
                "opened": 1,
                "clicked": 1,
                "complained": 1,
                "unsubscribed": 1,
            },
        },
    )

    client.broadcasts.retrieve(
        "550e8400-e29b-41d4-a716-446655440000",
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "GET"
    assert request.url.path == "/broadcasts/550e8400-e29b-41d4-a716-446655440000"


def test_list_failures(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        json={
            "totalCount": 1,
            "results": [
                {
                    "recipients": {"to": [{"email": "example"}]},
                    "messageIndex": 1,
                    "errorCode": "example",
                    "errorMessage": "example",
                }
            ],
        },
    )

    client.broadcasts.list_failures(
        "550e8400-e29b-41d4-a716-446655440000",
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "GET"
    assert request.url.path == "/broadcasts/550e8400-e29b-41d4-a716-446655440000/failures"


def test_list_suppressions(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        json={"totalCount": 1, "results": ["example"]},
    )

    client.broadcasts.list_suppressions(
        "550e8400-e29b-41d4-a716-446655440000",
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "GET"
    assert request.url.path == "/broadcasts/550e8400-e29b-41d4-a716-446655440000/suppressions"


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
                    "status": "accepted",
                    "subject": "example",
                    "completion": "example",
                    "messages": 1,
                }
            ],
        },
    )

    await async_client.broadcasts.list(
        channel_id="550e8400-e29b-41d4-a716-446655440000",
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.url.path == "/broadcasts"
