"""Integration tests that exercise the SDK against a live Helo API.

These are skipped by default. Run them with::

    pytest --integration

with ``HELO_API_KEY`` set in the environment. They target a local instance at
``http://localhost:8000`` by default; override with ``HELO_BASE_URL``.

Unlike the read-only smoke tests, this suite exercises the full surface area:
it creates, mutates, and deletes real resources, sends messages, and reads back
activity and statistics. Created resources use unique names and are cleaned up
in fixture teardown.

The API is eventually consistent, so reads that follow a write are wrapped in
``eventually(...)``, which retries until the assertion passes or a timeout is
reached. Tune the timing with ``HELO_POLL_TIMEOUT`` / ``HELO_POLL_INTERVAL``.
"""

from __future__ import annotations

import os
import time
import uuid
from collections.abc import Callable, Iterator
from typing import TypeVar

import pytest

import helo

pytestmark = pytest.mark.integration

T = TypeVar("T")

POLL_TIMEOUT = float(os.environ.get("HELO_POLL_TIMEOUT", "10"))
POLL_INTERVAL = float(os.environ.get("HELO_POLL_INTERVAL", "0.5"))


def eventually(
    fn: Callable[[], T],
    *,
    catch: tuple[type[BaseException], ...] = (AssertionError,),
    timeout: float = POLL_TIMEOUT,
    interval: float = POLL_INTERVAL,
) -> T:
    """Call ``fn`` until it returns without raising one of ``catch``.

    Retries on the listed exception types (assertion failures by default, so a
    ``list``-membership check can be polled directly) until ``timeout`` seconds
    have elapsed, then re-raises the last failure.
    """
    deadline = time.monotonic() + timeout
    while True:
        try:
            return fn()
        except catch:
            if time.monotonic() >= deadline:
                raise
        time.sleep(interval)


def _unique(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


# --------------------------------------------------------------------------- #
# Resource fixtures (create, wait for consistency, clean up)
# --------------------------------------------------------------------------- #


@pytest.fixture(scope="module")
def channel(live_client: helo.Helo) -> Iterator[helo.ChannelDetailsResponse]:
    created = live_client.channels.create(
        name=_unique("sdk-test"),
        delivery_type=helo.DeliveryType.SANDBOX,
    )
    # Wait until the new channel is readable before dependent tests use it.
    eventually(lambda: live_client.channels.retrieve(created.id), catch=(helo.NotFoundError,))
    try:
        yield created
    finally:
        try:
            live_client.channels.delete(created.id)
        except helo.NotFoundError:
            pass


@pytest.fixture(scope="module")
def domain(
    live_client: helo.Helo, channel: helo.ChannelDetailsResponse
) -> Iterator[helo.DomainWithDnsResponse]:
    created = live_client.domains.create(
        name=f"{_unique('mail')}.example.com",
        channel_ids=[channel.id],
    )
    eventually(lambda: live_client.domains.retrieve(created.id), catch=(helo.NotFoundError,))
    try:
        yield created
    finally:
        try:
            live_client.domains.delete(created.id)
        except helo.NotFoundError:
            pass


@pytest.fixture(scope="module")
def webhook(
    live_client: helo.Helo, channel: helo.ChannelDetailsResponse
) -> Iterator[helo.WebhookEndpointResponse]:
    created = live_client.webhook_endpoints.create(
        url="https://example.com/webhooks/helo",
        events=[helo.WebhookEvent.DELIVERED, helo.WebhookEvent.BOUNCED],
        channel_id=channel.id,
    )
    eventually(
        lambda: live_client.webhook_endpoints.retrieve(created.id),
        catch=(helo.NotFoundError,),
    )
    try:
        yield created
    finally:
        try:
            live_client.webhook_endpoints.delete(created.id)
        except helo.NotFoundError:
            pass


@pytest.fixture(scope="module")
def broadcast_id(live_client: helo.Helo, channel: helo.ChannelDetailsResponse) -> str:
    resp = live_client.sending.broadcast(
        from_={"email": "newsletter@example.com"},
        template={"subject": "Hello {{name}}", "html": "<p>Hi {{name}}</p>"},
        messages=[
            {"to": [{"email": "user1@example.com"}], "variables": {"name": "Alice"}},
            {"to": [{"email": "user2@example.com"}], "variables": {"name": "Bob"}},
        ],
        channel_id=channel.id,
    )
    assert resp.broadcast_id
    bid = resp.broadcast_id
    eventually(lambda: live_client.broadcasts.retrieve(bid), catch=(helo.NotFoundError,))
    return bid


# --------------------------------------------------------------------------- #
# Channels
# --------------------------------------------------------------------------- #


class TestChannels:
    def test_create_and_retrieve(
        self, live_client: helo.Helo, channel: helo.ChannelDetailsResponse
    ) -> None:
        fetched = live_client.channels.retrieve(channel.id)
        assert fetched.id == channel.id
        assert fetched.delivery_type == helo.DeliveryType.SANDBOX

    def test_update(self, live_client: helo.Helo, channel: helo.ChannelDetailsResponse) -> None:
        new_name = _unique("sdk-renamed")
        updated = live_client.channels.update(channel.id, name=new_name)
        assert updated.name == new_name

    def test_list_and_filter(
        self, live_client: helo.Helo, channel: helo.ChannelDetailsResponse
    ) -> None:
        def listed() -> None:
            page = live_client.channels.list(limit=50)
            assert any(c.id == channel.id for c in page.results)

        eventually(listed)

        filtered = live_client.channels.list(channel_ids=[channel.id])
        assert all(c.id == channel.id for c in filtered.results)

    def test_create_delete_roundtrip(self, live_client: helo.Helo) -> None:
        created = live_client.channels.create(
            name=_unique("sdk-ephemeral"),
            delivery_type=helo.DeliveryType.SANDBOX,
        )
        live_client.channels.delete(created.id)

        def gone() -> None:
            try:
                live_client.channels.retrieve(created.id)
            except helo.NotFoundError:
                return
            raise AssertionError("channel still present after delete")

        eventually(gone)


# --------------------------------------------------------------------------- #
# Sending
# --------------------------------------------------------------------------- #


class TestSending:
    def test_transactional(
        self, live_client: helo.Helo, channel: helo.ChannelDetailsResponse
    ) -> None:
        resp = live_client.sending.transactional(
            from_={"email": "sender@example.com", "name": "SDK Test"},
            to=[{"email": "recipient@example.com"}],
            subject="Integration test",
            html="<p>Hello</p>",
            text="Hello",
            tags=["integration"],
            channel_id=channel.id,
            idempotency_key=_unique("idem"),
        )
        assert resp.message_id

    def test_transactional_batch(
        self, live_client: helo.Helo, channel: helo.ChannelDetailsResponse
    ) -> None:
        resp = live_client.sending.transactional_batch(
            requests=[
                {
                    "from": {"email": "sender@example.com"},
                    "to": [{"email": "user1@example.com"}],
                    "subject": "Batch 1",
                    "text": "Hi 1",
                },
                {
                    "from": {"email": "sender@example.com"},
                    "to": [{"email": "user2@example.com"}],
                    "subject": "Batch 2",
                    "text": "Hi 2",
                },
            ],
            channel_id=channel.id,
        )
        assert len(resp.responses) == 2

    def test_broadcast_message(
        self, live_client: helo.Helo, channel: helo.ChannelDetailsResponse
    ) -> None:
        resp = live_client.sending.broadcast_message(
            from_={"email": "newsletter@example.com"},
            to=[{"email": "user@example.com"}],
            subject="Digest",
            html="<p>News</p>",
            channel_id=channel.id,
        )
        assert resp.message_id


# --------------------------------------------------------------------------- #
# Activity
# --------------------------------------------------------------------------- #


class TestActivity:
    def test_list_messages(
        self, live_client: helo.Helo, channel: helo.ChannelDetailsResponse
    ) -> None:
        result = live_client.activity.list_messages(channel_id=channel.id, limit=10)
        assert isinstance(result.results, list)

    def test_list_events(
        self, live_client: helo.Helo, channel: helo.ChannelDetailsResponse
    ) -> None:
        result = live_client.activity.list_events(
            channel_id=channel.id,
            event_types=[helo.EventType.ACCEPTED, helo.EventType.DELIVERED],
            limit=10,
        )
        assert isinstance(result.results, list)

    def test_send_then_retrieve_message(
        self, live_client: helo.Helo, channel: helo.ChannelDetailsResponse
    ) -> None:
        sent = live_client.sending.transactional(
            from_={"email": "sender@example.com"},
            to=[{"email": "lookup@example.com"}],
            subject="Lookup",
            text="Lookup",
            channel_id=channel.id,
        )
        message_id = sent.message_id
        assert message_id
        message = eventually(
            lambda: live_client.activity.retrieve_message(message_id),
            catch=(helo.NotFoundError,),
        )
        assert message.message_id == message_id


# --------------------------------------------------------------------------- #
# Domains
# --------------------------------------------------------------------------- #


class TestDomains:
    def test_retrieve(self, live_client: helo.Helo, domain: helo.DomainWithDnsResponse) -> None:
        fetched = live_client.domains.retrieve(domain.id)
        assert fetched.id == domain.id

    def test_list(self, live_client: helo.Helo, domain: helo.DomainWithDnsResponse) -> None:
        def listed() -> None:
            page = live_client.domains.list(limit=50)
            assert any(d.id == domain.id for d in page.results)

        eventually(listed)

    def test_update_channels(
        self,
        live_client: helo.Helo,
        domain: helo.DomainWithDnsResponse,
        channel: helo.ChannelDetailsResponse,
    ) -> None:
        updated = live_client.domains.update(domain.id, channel_ids=[channel.id])
        assert updated.id == domain.id

    def test_verify(self, live_client: helo.Helo, domain: helo.DomainWithDnsResponse) -> None:
        records = live_client.domains.verify(domain.id)
        assert records is not None

    def test_rotate_key(
        self, live_client: helo.Helo, domain: helo.DomainWithDnsResponse
    ) -> None:
        record = live_client.domains.rotate_key(domain.id)
        assert record is not None


# --------------------------------------------------------------------------- #
# Broadcasts
# --------------------------------------------------------------------------- #


class TestBroadcasts:
    def test_list(
        self, live_client: helo.Helo, channel: helo.ChannelDetailsResponse, broadcast_id: str
    ) -> None:
        def listed() -> None:
            page = live_client.broadcasts.list(channel_id=channel.id, limit=50)
            assert any(b.id == broadcast_id for b in page.results)

        eventually(listed)

    def test_retrieve(self, live_client: helo.Helo, broadcast_id: str) -> None:
        broadcast = live_client.broadcasts.retrieve(broadcast_id)
        assert broadcast.id == broadcast_id

    def test_list_failures(self, live_client: helo.Helo, broadcast_id: str) -> None:
        failures = live_client.broadcasts.list_failures(broadcast_id)
        assert isinstance(failures.results, list)

    def test_list_suppressions(self, live_client: helo.Helo, broadcast_id: str) -> None:
        suppressions = live_client.broadcasts.list_suppressions(broadcast_id)
        assert isinstance(suppressions.results, list)


# --------------------------------------------------------------------------- #
# Statistics
# --------------------------------------------------------------------------- #


class TestStatistics:
    def test_totals(self, live_client: helo.Helo, channel: helo.ChannelDetailsResponse) -> None:
        totals = live_client.statistics.retrieve_totals(
            from_="2024-01-01", to="2024-12-31", channel_id=channel.id
        )
        assert totals is not None

    def test_daily(self, live_client: helo.Helo, channel: helo.ChannelDetailsResponse) -> None:
        daily = live_client.statistics.retrieve_daily(
            from_="2024-01-01",
            to="2024-12-31",
            timezone="America/New_York",
            channel_id=channel.id,
        )
        assert daily is not None

    def test_hourly(self, live_client: helo.Helo, channel: helo.ChannelDetailsResponse) -> None:
        hourly = live_client.statistics.retrieve_hourly(
            from_="2024-01-01T00:00:00Z",
            to="2024-01-01T23:59:59Z",
            channel_id=channel.id,
        )
        assert hourly is not None


# --------------------------------------------------------------------------- #
# Suppressions
# --------------------------------------------------------------------------- #


class TestSuppressions:
    def test_create_list_remove(
        self, live_client: helo.Helo, channel: helo.ChannelDetailsResponse
    ) -> None:
        email = f"{_unique('suppressed')}@example.com"

        live_client.suppressions.create(
            channel_id=channel.id,
            mail_type=helo.MailType.TRANSACTIONAL,
            emails=[email],
        )

        def present() -> None:
            page = live_client.suppressions.list(
                channel_id=channel.id, mail_type=helo.MailType.TRANSACTIONAL, email=email
            )
            assert any(s.email == email for s in page.results)

        eventually(present)

        live_client.suppressions.remove(
            channel_id=channel.id,
            mail_type=helo.MailType.TRANSACTIONAL,
            emails=[email],
        )

        def absent() -> None:
            page = live_client.suppressions.list(
                channel_id=channel.id, mail_type=helo.MailType.TRANSACTIONAL, email=email
            )
            assert all(s.email != email for s in page.results)

        eventually(absent)


# --------------------------------------------------------------------------- #
# Webhook endpoints
# --------------------------------------------------------------------------- #


class TestWebhookEndpoints:
    def test_create_and_retrieve(
        self, live_client: helo.Helo, webhook: helo.WebhookEndpointResponse
    ) -> None:
        fetched = live_client.webhook_endpoints.retrieve(webhook.id)
        assert fetched.id == webhook.id

    def test_list(self, live_client: helo.Helo, webhook: helo.WebhookEndpointResponse) -> None:
        def listed() -> None:
            page = live_client.webhook_endpoints.list(limit=50)
            assert any(w.id == webhook.id for w in page.results)

        eventually(listed)

    def test_update(
        self, live_client: helo.Helo, webhook: helo.WebhookEndpointResponse
    ) -> None:
        updated = live_client.webhook_endpoints.update(webhook.id, enabled=False)
        assert updated.enabled is False

    def test_regenerate_signing_key(
        self, live_client: helo.Helo, webhook: helo.WebhookEndpointResponse
    ) -> None:
        rotated = live_client.webhook_endpoints.regenerate_signing_key(webhook.id)
        assert rotated.id == webhook.id


# --------------------------------------------------------------------------- #
# Auth
# --------------------------------------------------------------------------- #


class TestAuth:
    def test_invalid_key_raises(self) -> None:
        base_url = os.environ.get("HELO_BASE_URL", "http://localhost:8000")
        client = helo.Helo(api_key="obviously-invalid-key", base_url=base_url)
        with pytest.raises(helo.AuthenticationError):
            client.channels.list(limit=1)
