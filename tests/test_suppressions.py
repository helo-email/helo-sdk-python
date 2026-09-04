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
                    "email": "example",
                    "reason": "bounce",
                    "createdAt": "2024-01-01T00:00:00Z",
                }
            ],
        },
    )

    client.suppressions.list(
        channel_id="550e8400-e29b-41d4-a716-446655440000",
        mail_type=helo.MailType.TRANSACTIONAL,
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "GET"
    assert request.url.path == "/suppressions"


def test_create(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        json={"results": [{"email": "example", "success": True}]},
    )

    client.suppressions.create(
        channel_id="550e8400-e29b-41d4-a716-446655440000",
        mail_type=helo.MailType.TRANSACTIONAL,
        emails=["test@example.com"],
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "POST"
    assert request.url.path == "/suppressions"


def test_remove(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        json={"results": [{"email": "example", "success": True}]},
    )

    client.suppressions.remove(
        channel_id="550e8400-e29b-41d4-a716-446655440000",
        mail_type=helo.MailType.TRANSACTIONAL,
        emails=["test@example.com"],
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "POST"
    assert request.url.path == "/suppressions/remove"


async def test_list_async(async_client: helo.AsyncHelo, httpx_mock: HTTPXMock) -> None:
    """The async resource is generated from the same operation, so one call proves the pair."""
    httpx_mock.add_response(
        method="GET",
        json={
            "totalCount": 1,
            "results": [
                {
                    "email": "example",
                    "reason": "bounce",
                    "createdAt": "2024-01-01T00:00:00Z",
                }
            ],
        },
    )

    await async_client.suppressions.list(
        channel_id="550e8400-e29b-41d4-a716-446655440000",
        mail_type=helo.MailType.TRANSACTIONAL,
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.url.path == "/suppressions"
