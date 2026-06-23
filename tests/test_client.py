from __future__ import annotations

import json as json_lib

import pytest
from pytest_httpx import HTTPXMock

import sdk_helo_email
from sdk_helo_email import AsyncHelo, DeliveryType, Helo, WebhookEvent

BASE_URL = "http://localhost:8000"


@pytest.fixture
def client(httpx_mock: HTTPXMock) -> Helo:
    return Helo(api_key="test-key", base_url=BASE_URL)


@pytest.fixture
def async_client(httpx_mock: HTTPXMock) -> AsyncHelo:
    return AsyncHelo(api_key="test-key", base_url=BASE_URL)


class TestChannels:
    def test_create(self, client: Helo, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            method="POST",
            url=f"{BASE_URL}/channels",
            json={
                "id": "channel-1",
                "name": "test",
                "deliveryType": "live",
                "createdAt": "2024-01-01T00:00:00Z",
                "updatedAt": "2024-01-01T00:00:00Z",
                "tracking": {"links": True, "opens": True},
            },
        )
        result = client.channels.create(name="test", delivery_type=DeliveryType.LIVE)
        assert result.id == "channel-1"
        assert result.name == "test"
        assert result.delivery_type == DeliveryType.LIVE
        assert result.tracking.links is True

    def test_list(self, client: Helo, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            method="GET",
            url=f"{BASE_URL}/channels",
            json={
                "results": [
                    {
                        "id": "channel-1",
                        "name": "test",
                        "deliveryType": "live",
                        "createdAt": "2024-01-01T00:00:00Z",
                    }
                ],
                "totalCount": 1,
            },
        )
        result = client.channels.list()
        assert result.total_count == 1
        assert len(result.results) == 1
        assert result.results[0].id == "channel-1"

    def test_list_with_channel_ids(self, client: Helo, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            method="GET",
            url=f"{BASE_URL}/channels?channelIds=a,b",
            json={"results": [], "totalCount": 0},
        )
        client.channels.list(channel_ids=["a", "b"])
        request = httpx_mock.get_request()
        assert request is not None
        assert request.url.params["channelIds"] == "a,b"

    def test_retrieve(self, client: Helo, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            method="GET",
            url=f"{BASE_URL}/channels/channel-1",
            json={
                "id": "channel-1",
                "name": "test",
                "deliveryType": "sandbox",
                "createdAt": "2024-01-01T00:00:00Z",
                "updatedAt": "2024-01-01T00:00:00Z",
                "tracking": {"links": False, "opens": True},
            },
        )
        result = client.channels.retrieve("channel-1")
        assert result.id == "channel-1"
        assert result.delivery_type == DeliveryType.SANDBOX

    def test_delete(self, client: Helo, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            method="DELETE", url=f"{BASE_URL}/channels/channel-1", status_code=204
        )
        client.channels.delete("channel-1")


class TestSending:
    def test_transactional(self, client: Helo, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            method="POST",
            url=f"{BASE_URL}/send/transactional",
            json={"status": "accepted", "messageId": "msg-1", "suppressions": []},
        )
        result = client.sending.transactional(
            from_={"email": "sender@example.com", "name": "Sender"},
            to=[{"email": "recipient@example.com"}],
            subject="Hello",
            html="<p>Hello</p>",
        )
        assert result.status == "accepted"
        assert result.message_id == "msg-1"

    def test_transactional_body_uses_api_keys(self, client: Helo, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            method="POST",
            url=f"{BASE_URL}/send/transactional",
            json={"status": "accepted", "messageId": "msg-1"},
        )
        client.sending.transactional(
            from_={"email": "sender@example.com"},
            to=[{"email": "recipient@example.com"}],
            reply_to=[{"email": "reply@example.com"}],
            subject="Hello",
        )
        request = httpx_mock.get_request()
        assert request is not None
        body = json_lib.loads(request.content)
        # from_ -> "from", reply_to -> "replyTo"
        assert body["from"] == {"email": "sender@example.com"}
        assert body["replyTo"] == [{"email": "reply@example.com"}]

    def test_transactional_with_channel_id(self, client: Helo, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            method="POST",
            url=f"{BASE_URL}/send/transactional",
            json={"status": "accepted", "messageId": "msg-2"},
        )
        result = client.sending.transactional(
            from_={"email": "sender@example.com"},
            to=[{"email": "recipient@example.com"}],
            subject="Test",
            channel_id="channel-1",
            idempotency_key="unique-key-123",
        )
        assert result.message_id == "msg-2"
        request = httpx_mock.get_request()
        assert request is not None
        assert request.headers.get("X-Helo-Channel-Id") == "channel-1"
        assert request.headers.get("X-Helo-Idempotency-Key") == "unique-key-123"


class TestErrors:
    def test_authentication_error(self, httpx_mock: HTTPXMock) -> None:
        client = Helo(api_key="test-key", base_url=BASE_URL)
        httpx_mock.add_response(
            method="GET",
            url=f"{BASE_URL}/channels",
            status_code=401,
            json={"title": "Unauthorized", "status": 401, "code": "unauthorized"},
        )
        with pytest.raises(sdk_helo_email.AuthenticationError) as exc_info:
            client.channels.list()
        assert exc_info.value.status_code == 401
        assert exc_info.value.error_code == "unauthorized"

    def test_not_found_error(self, httpx_mock: HTTPXMock) -> None:
        client = Helo(api_key="test-key", base_url=BASE_URL)
        httpx_mock.add_response(
            method="GET",
            url=f"{BASE_URL}/channels/missing",
            status_code=404,
            json={"title": "Not Found", "status": 404},
        )
        with pytest.raises(sdk_helo_email.NotFoundError):
            client.channels.retrieve("missing")

    def test_conflict_error(self, httpx_mock: HTTPXMock) -> None:
        client = Helo(api_key="test-key", base_url=BASE_URL, max_retries=0)
        httpx_mock.add_response(
            method="POST",
            url=f"{BASE_URL}/channels",
            status_code=409,
            json={"title": "Conflict", "status": 409},
        )
        with pytest.raises(sdk_helo_email.ConflictError):
            client.channels.create(name="dupe", delivery_type=DeliveryType.LIVE)

    def test_rate_limit_error_exposes_retry_after(self, httpx_mock: HTTPXMock) -> None:
        client = Helo(api_key="test-key", base_url=BASE_URL, max_retries=0)
        httpx_mock.add_response(
            method="GET",
            url=f"{BASE_URL}/channels",
            status_code=429,
            headers={"Retry-After": "12"},
            json={"title": "Too Many Requests", "status": 429},
        )
        with pytest.raises(sdk_helo_email.RateLimitError) as exc_info:
            client.channels.list()
        assert exc_info.value.status_code == 429
        assert exc_info.value.retry_after == 12.0


class TestRetries:
    def test_retries_on_server_error(
        self, httpx_mock: HTTPXMock, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(sdk_helo_email._http, "_backoff_delay", lambda *a, **k: 0.0)
        client = Helo(api_key="test-key", base_url=BASE_URL, max_retries=2)
        httpx_mock.add_response(method="GET", url=f"{BASE_URL}/channels", status_code=503)
        httpx_mock.add_response(
            method="GET",
            url=f"{BASE_URL}/channels",
            json={"results": [], "totalCount": 0},
        )
        result = client.channels.list()
        assert result.total_count == 0
        assert len(httpx_mock.get_requests()) == 2

    def test_gives_up_after_max_retries(
        self, httpx_mock: HTTPXMock, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(sdk_helo_email._http, "_backoff_delay", lambda *a, **k: 0.0)
        client = Helo(api_key="test-key", base_url=BASE_URL, max_retries=1)
        httpx_mock.add_response(method="GET", url=f"{BASE_URL}/channels", status_code=500)
        httpx_mock.add_response(method="GET", url=f"{BASE_URL}/channels", status_code=500)
        with pytest.raises(sdk_helo_email.InternalServerError):
            client.channels.list()
        assert len(httpx_mock.get_requests()) == 2


class TestWebhookEndpoints:
    def test_create(self, client: Helo, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            method="POST",
            url=f"{BASE_URL}/webhook-endpoints",
            json={
                "id": "wh-1",
                "url": "https://example.com/webhook",
                "events": ["delivered", "bounced"],
                "enabled": True,
                "payloadSigningKey": "signing-key-abc",
            },
        )
        result = client.webhook_endpoints.create(
            url="https://example.com/webhook",
            events=[WebhookEvent.DELIVERED, WebhookEvent.BOUNCED],
        )
        assert result.id == "wh-1"
        assert result.enabled is True


class TestAsyncClient:
    async def test_create_channel(self, async_client: AsyncHelo, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            method="POST",
            url=f"{BASE_URL}/channels",
            json={
                "id": "channel-1",
                "name": "test",
                "deliveryType": "live",
                "createdAt": "2024-01-01T00:00:00Z",
                "updatedAt": "2024-01-01T00:00:00Z",
                "tracking": {"links": True, "opens": True},
            },
        )
        async with async_client as client:
            result = await client.channels.create(name="test", delivery_type=DeliveryType.LIVE)
        assert result.id == "channel-1"
        assert result.delivery_type == DeliveryType.LIVE

    async def test_async_not_found_error(
        self, async_client: AsyncHelo, httpx_mock: HTTPXMock
    ) -> None:
        httpx_mock.add_response(
            method="GET",
            url=f"{BASE_URL}/channels/missing",
            status_code=404,
            json={"title": "Not Found", "status": 404},
        )
        async with async_client as client:
            with pytest.raises(sdk_helo_email.NotFoundError):
                await client.channels.retrieve("missing")
