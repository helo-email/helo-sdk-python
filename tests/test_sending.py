from __future__ import annotations

from pytest_httpx import HTTPXMock

import sdk_helo_email as helo


def test_transactional(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        json={},
    )

    client.sending.transactional(
        from_={"email": "from@yourdomain.com", "name": "From name"},
        to=[{"email": "to@example.com", "name": "To name"}],
        cc=[{"email": "cc@example.com", "name": "Cc name"}],
        bcc=[{"email": "bcc@example.com", "name": "Bcc name"}],
        reply_to=[{"email": "reply-to@example.com", "name": "Reply-To name"}],
        subject="Hello from Helo",
        html="<html><body><h1>Hi there, new friend.</h1><p>This is a test message, delivered with <3 by Helo. </p></body></html>",
        text="This is a test message, delivered with <3 by Helo.",
        template={
            "subject": "test-subject",
            "html": "test-html",
            "text": "test-text",
            "inlineStyles": True,
        },
        tracking={"opens": True, "links": True},
        attachments=[
            {
                "content": "SGVsbG8gd29ybGQ=",
                "contentId": "test-contentId",
                "contentType": "test-contentType",
                "fileName": "test-fileName",
                "disposition": helo.AttachmentDisposition.ATTACHMENT,
            },
        ],
        tags=["welcome", "onboarding"],
        channel_id="550e8400-e29b-41d4-a716-446655440000",
        idempotency_key="test-idempotency_key",
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "POST"
    assert request.url.path == "/send/transactional"
    assert "X-Helo-Channel-Id" in request.headers
    assert "X-Helo-Idempotency-Key" in request.headers


def test_transactional_batch(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        json={"responses": [{"status": "example"}]},
    )

    client.sending.transactional_batch(
        requests=[
            {
                "from": {"email": "from@yourdomain.com", "name": "From name"},
                "to": [{"email": "to@example.com", "name": "To name"}],
                "subject": "Hello from Helo",
                "html": "<html><body><h1>Hi there, new friend.</h1><p>This is a test message, delivered with <3 by Helo. </p></body></html>",
                "text": "This is a test message, delivered with <3 by Helo.",
                "tags": ["welcome", "onboarding"],
            },
        ],
        channel_id="550e8400-e29b-41d4-a716-446655440000",
        idempotency_key="test-idempotency_key",
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "POST"
    assert request.url.path == "/send/transactional/batch"
    assert "X-Helo-Channel-Id" in request.headers
    assert "X-Helo-Idempotency-Key" in request.headers


def test_broadcast(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        json={},
    )

    client.sending.broadcast(
        from_={"email": "test@example.com", "name": "test-name"},
        template={
            "subject": "test-subject",
            "html": "test-html",
            "text": "test-text",
            "inlineStyles": True,
        },
        messages=[
            {
                "to": [{"email": "test@example.com", "name": "test-name"}],
                "tags": ["test-tag"],
            },
        ],
        reply_to=[{"email": "test@example.com", "name": "test-name"}],
        tracking={"opens": True, "links": True},
        attachments=[
            {
                "content": "SGVsbG8gd29ybGQ=",
                "contentId": "test-contentId",
                "contentType": "test-contentType",
                "fileName": "test-fileName",
                "disposition": helo.AttachmentDisposition.ATTACHMENT,
            },
        ],
        tags=["test-tag"],
        channel_id="550e8400-e29b-41d4-a716-446655440000",
        idempotency_key="test-idempotency_key",
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "POST"
    assert request.url.path == "/send/broadcast"
    assert "X-Helo-Channel-Id" in request.headers
    assert "X-Helo-Idempotency-Key" in request.headers


def test_broadcast_message(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        json={},
    )

    client.sending.broadcast_message(
        from_={"email": "from@yourdomain.com", "name": "From name"},
        to=[{"email": "to@example.com", "name": "To name"}],
        cc=[{"email": "cc@example.com", "name": "Cc name"}],
        bcc=[{"email": "bcc@example.com", "name": "Bcc name"}],
        reply_to=[{"email": "reply-to@example.com", "name": "Reply-To name"}],
        subject="Hello from Helo",
        html="<html><body><h1>Hi there, new friend.</h1><p>This is a test message, delivered with <3 by Helo. </p></body></html>",
        text="This is a test message, delivered with <3 by Helo.",
        template={
            "subject": "test-subject",
            "html": "test-html",
            "text": "test-text",
            "inlineStyles": True,
        },
        tracking={"opens": True, "links": True},
        attachments=[
            {
                "content": "SGVsbG8gd29ybGQ=",
                "contentId": "test-contentId",
                "contentType": "test-contentType",
                "fileName": "test-fileName",
                "disposition": helo.AttachmentDisposition.ATTACHMENT,
            },
        ],
        tags=["welcome", "onboarding"],
        channel_id="550e8400-e29b-41d4-a716-446655440000",
        idempotency_key="test-idempotency_key",
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "POST"
    assert request.url.path == "/send/broadcast/message"
    assert "X-Helo-Channel-Id" in request.headers
    assert "X-Helo-Idempotency-Key" in request.headers


async def test_transactional_async(async_client: helo.AsyncHelo, httpx_mock: HTTPXMock) -> None:
    """The async resource is generated from the same operation, so one call proves the pair."""
    httpx_mock.add_response(
        method="POST",
        json={},
    )

    await async_client.sending.transactional(
        from_={"email": "from@yourdomain.com", "name": "From name"},
        to=[{"email": "to@example.com", "name": "To name"}],
        cc=[{"email": "cc@example.com", "name": "Cc name"}],
        bcc=[{"email": "bcc@example.com", "name": "Bcc name"}],
        reply_to=[{"email": "reply-to@example.com", "name": "Reply-To name"}],
        subject="Hello from Helo",
        html="<html><body><h1>Hi there, new friend.</h1><p>This is a test message, delivered with <3 by Helo. </p></body></html>",
        text="This is a test message, delivered with <3 by Helo.",
        template={
            "subject": "test-subject",
            "html": "test-html",
            "text": "test-text",
            "inlineStyles": True,
        },
        tracking={"opens": True, "links": True},
        attachments=[
            {
                "content": "SGVsbG8gd29ybGQ=",
                "contentId": "test-contentId",
                "contentType": "test-contentType",
                "fileName": "test-fileName",
                "disposition": helo.AttachmentDisposition.ATTACHMENT,
            },
        ],
        tags=["welcome", "onboarding"],
        channel_id="550e8400-e29b-41d4-a716-446655440000",
        idempotency_key="test-idempotency_key",
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.url.path == "/send/transactional"
