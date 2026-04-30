from __future__ import annotations

import pytest
import httpx
from pytest_httpx import HTTPXMock

import helo
from helo import Helo, DeliveryType, MailType, WebhookEvent


BASE_URL = "http://localhost:8002"


@pytest.fixture
def client(httpx_mock: HTTPXMock) -> Helo:
    return Helo(api_key="test-key", base_url=BASE_URL)


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
        httpx_mock.add_response(method="DELETE", url=f"{BASE_URL}/channels/channel-1", status_code=204)
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
    def test_authentication_error(self, client: Helo, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            method="GET",
            url=f"{BASE_URL}/channels",
            status_code=401,
            json={"title": "Unauthorized", "status": 401, "code": "unauthorized"},
        )
        with pytest.raises(helo.AuthenticationError) as exc_info:
            client.channels.list()
        assert exc_info.value.status_code == 401

    def test_not_found_error(self, client: Helo, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            method="GET",
            url=f"{BASE_URL}/channels/missing",
            status_code=404,
            json={"title": "Not Found", "status": 404},
        )
        with pytest.raises(helo.NotFoundError):
            client.channels.retrieve("missing")


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
