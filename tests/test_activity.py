from __future__ import annotations

from pytest_httpx import HTTPXMock

import sdk_helo_email as helo


def test_list_events(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        json={
            "totalCount": 1.0,
            "results": [
                {
                    "messageId": "550e8400-e29b-41d4-a716-446655440000",
                    "channelId": "550e8400-e29b-41d4-a716-446655440000",
                    "mailType": "transactional",
                    "eventType": "accepted",
                    "timestamp": "2024-01-01T00:00:00Z",
                    "subject": "example",
                    "recipients": ["example"],
                }
            ],
        },
    )

    client.activity.list_events()

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "GET"
    assert request.url.path == "/activity/events"


def test_list_messages(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        json={
            "totalCount": 1.0,
            "results": [
                {
                    "messageId": "550e8400-e29b-41d4-a716-446655440000",
                    "channelId": "550e8400-e29b-41d4-a716-446655440000",
                    "timestamp": "2024-01-01T00:00:00Z",
                    "mailType": "transactional",
                    "mailSource": "api",
                    "deliveryType": "live",
                    "status": "queued",
                    "subject": "example",
                    "recipients": ["example"],
                    "statistics": {
                        "delivered": 1,
                        "bounced": 1,
                        "opened": 1,
                        "clicked": 1,
                        "complained": 1,
                        "unsubscribed": 1,
                    },
                }
            ],
        },
    )

    client.activity.list_messages()

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "GET"
    assert request.url.path == "/activity/messages"


def test_retrieve_message(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        json={
            "messageId": "550e8400-e29b-41d4-a716-446655440000",
            "channelId": "550e8400-e29b-41d4-a716-446655440000",
            "timestamp": "2024-01-01T00:00:00Z",
            "mailType": "transactional",
            "mailSource": "api",
            "deliveryType": "live",
            "status": "queued",
            "subject": "example",
            "from": {"email": "test@example.com"},
            "to": [{"email": "test@example.com"}],
            "tracking": {"links": True, "opens": True},
            "events": [
                {
                    "eventType": "accepted",
                    "timestamp": "2024-01-01T00:00:00Z",
                    "recipients": ["example"],
                }
            ],
        },
    )

    client.activity.retrieve_message(
        "550e8400-e29b-41d4-a716-446655440000",
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "GET"
    assert request.url.path == "/activity/messages/550e8400-e29b-41d4-a716-446655440000"


async def test_list_events_async(async_client: helo.AsyncHelo, httpx_mock: HTTPXMock) -> None:
    """The async resource is generated from the same operation, so one call proves the pair."""
    httpx_mock.add_response(
        method="GET",
        json={
            "totalCount": 1.0,
            "results": [
                {
                    "messageId": "550e8400-e29b-41d4-a716-446655440000",
                    "channelId": "550e8400-e29b-41d4-a716-446655440000",
                    "mailType": "transactional",
                    "eventType": "accepted",
                    "timestamp": "2024-01-01T00:00:00Z",
                    "subject": "example",
                    "recipients": ["example"],
                }
            ],
        },
    )

    await async_client.activity.list_events()

    request = httpx_mock.get_request()
    assert request is not None
    assert request.url.path == "/activity/events"
