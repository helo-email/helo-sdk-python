"""The retry policy every Helo SDK shares, and the request details it relies on."""

from __future__ import annotations

import json
import re

import httpx
import pytest
from pytest_httpx import HTTPXMock

import sdk_helo_email as helo
from sdk_helo_email import _http
from sdk_helo_email._http import HttpClient

BASE_URL = "https://api.example.test"


@pytest.fixture(autouse=True)
def no_backoff(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(_http, "_backoff_delay", lambda attempt: 0.0)


@pytest.fixture
def http() -> HttpClient:
    return HttpClient(api_key="test-key", base_url=BASE_URL)


def test_retries_an_idempotent_request(http: HttpClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(status_code=503)
    httpx_mock.add_response(json={"ok": True})

    assert http.get("/things") == {"ok": True}
    assert len(httpx_mock.get_requests()) == 2


def test_retries_a_post_carrying_an_idempotency_key(
    http: HttpClient, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_response(status_code=502)
    httpx_mock.add_response(json={"ok": True})

    http.post("/things", json={}, headers={"X-Example-Idempotency-Key": "key-1"})

    keys = [r.headers["X-Example-Idempotency-Key"] for r in httpx_mock.get_requests()]
    assert keys == ["key-1", "key-1"]


# Without a key, the server may have acted on the first attempt before failing.
def test_does_not_retry_a_post_without_an_idempotency_key(
    http: HttpClient, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_response(status_code=503)

    with pytest.raises(helo.InternalServerError):
        http.post("/things", json={})
    assert len(httpx_mock.get_requests()) == 1


def test_does_not_retry_a_post_without_a_key_after_a_network_error(
    http: HttpClient, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_exception(httpx.ReadTimeout("timed out"))

    with pytest.raises(helo.APITimeoutError):
        http.post("/things", json={})
    assert len(httpx_mock.get_requests()) == 1


def test_retries_a_network_error_on_an_idempotent_request(
    http: HttpClient, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_exception(httpx.ConnectError("refused"))
    httpx_mock.add_response(json={"ok": True})

    assert http.get("/things") == {"ok": True}


# A 429 means the server refused the request without acting on it.
def test_retries_a_rate_limited_post_even_without_a_key(
    http: HttpClient, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_response(status_code=429, headers={"Retry-After": "0"})
    httpx_mock.add_response(json={"ok": True})

    assert http.post("/things", json={}) == {"ok": True}


def test_does_not_retry_early_when_retry_after_is_longer_than_it_waits(
    http: HttpClient, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_response(status_code=429, headers={"Retry-After": "60"})

    with pytest.raises(helo.RateLimitError) as raised:
        http.get("/things")
    assert raised.value.retry_after == 60.0
    assert len(httpx_mock.get_requests()) == 1


def test_gives_up_after_max_retries(httpx_mock: HTTPXMock) -> None:
    http = HttpClient(api_key="test-key", base_url=BASE_URL, max_retries=1)
    httpx_mock.add_response(status_code=500)
    httpx_mock.add_response(status_code=500)

    with pytest.raises(helo.InternalServerError):
        http.get("/things")
    assert len(httpx_mock.get_requests()) == 2


def test_max_retries_zero_disables_retries(httpx_mock: HTTPXMock) -> None:
    http = HttpClient(api_key="test-key", base_url=BASE_URL, max_retries=0)
    httpx_mock.add_response(status_code=503)

    with pytest.raises(helo.InternalServerError):
        http.get("/things")


# A send whose response is lost must not be sent twice: the SDK generates a key
# when the caller doesn't pass one, and reuses it on the retry.
def test_generates_one_idempotency_key_per_call(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(status_code=503)
    httpx_mock.add_response(json={})

    client.sending.send_transactional(
        from_={"email": "from@yourdomain.com", "name": "From name"},
        to=[{"email": "to@example.com", "name": "To name"}],
        cc=[{"email": "cc@example.com", "name": "Cc name"}],
        bcc=[{"email": "bcc@example.com", "name": "Bcc name"}],
        reply_to=[{"email": "reply-to@example.com", "name": "Reply-To name"}],
        subject="Hello from Helo",
        html="<html><body><h1>Hi there, new friend.</h1><p>This is a test message, delivered with <3 by Helo. </p></body></html>",
        text="This is a test message, delivered with <3 by Helo.",
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
    )

    keys = [r.headers["X-Helo-Idempotency-Key"] for r in httpx_mock.get_requests()]
    assert len(keys) == 2
    assert keys[0] == keys[1]
    assert re.fullmatch(r"[0-9a-f-]{36}", keys[0])


# Leaving an argument out can't clear a field; naming it in null_fields sends null.
def test_null_fields_sends_null(client: helo.Helo, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        json={
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "createdAt": "2024-01-01T00:00:00Z",
            "updatedAt": "2024-01-01T00:00:00Z",
            "version": 1,
            "name": "example",
            "subject": "example",
        }
    )

    client.templates.update(
        "550e8400-e29b-41d4-a716-446655440000",
        name="test-name",
        subject="test-subject",
        html="test-html",
        mjml="test-mjml",
        text="test-text",
        channel_ids=["550e8400-e29b-41d4-a716-446655440000"],
        version=10,
        null_fields=["html"],
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert json.loads(request.content)["html"] is None


def test_null_fields_rejects_a_field_that_cannot_be_null(client: helo.Helo) -> None:
    with pytest.raises(ValueError, match="can't be null"):
        client.templates.update(
            "550e8400-e29b-41d4-a716-446655440000",
            name="test-name",
            subject="test-subject",
            html="test-html",
            mjml="test-mjml",
            text="test-text",
            channel_ids=["550e8400-e29b-41d4-a716-446655440000"],
            version=10,
            null_fields=["not_a_field"],
        )


# A value the API added after this SDK version was released still parses.
def test_an_enum_accepts_a_value_this_version_does_not_know() -> None:
    value = helo.AttachmentDisposition("added-later")

    assert value == "added-later"
    assert isinstance(value, helo.AttachmentDisposition)
    assert helo.AttachmentDisposition("attachment") is helo.AttachmentDisposition.ATTACHMENT
