# Helo Python SDK

Python client library for the [Helo](https://helohq.com) email API.

## Installation

```bash
pip install sdk_helo_email
```

Requires Python 3.10+ and installs `httpx` and `pydantic` automatically.

## Quick Start

```python
import sdk_helo_email

# API key is read from the HELO_API_KEY environment variable automatically
client = sdk_helo_email.Helo()

response = client.sending.transactional(
    from_={"email": "sender@example.com", "name": "Acme"},
    to=[{"email": "user@example.com", "name": "Alice"}],
    subject="Hello from Helo",
    html="<p>Welcome!</p>",
    text="Welcome!",
)
print(response.message_id)
```

## Authentication

Set the `HELO_API_KEY` environment variable and the client picks it up automatically:

```bash
export HELO_API_KEY="your-api-key"
```

```python
client = sdk_helo_email.Helo()
```

You can also pass the key explicitly — useful when managing multiple accounts or reading from a secrets manager:

```python
client = sdk_helo_email.Helo(api_key="your-api-key")
```

Optionally override the base URL, timeout, or retry count (defaults: `https://api.helohq.com`, 30 seconds, 2 retries):

```python
client = sdk_helo_email.Helo(
    base_url="https://api.helohq.com",
    timeout=60.0,
    max_retries=2,
)
```

## Context Manager

Use `with` to ensure the underlying HTTP connection is closed:

```python
with sdk_helo_email.Helo() as client:
    client.sending.transactional(...)
```

## Async

An `AsyncHelo` client mirrors the synchronous API; every resource method becomes
a coroutine. Use it as an async context manager so the connection pool is closed:

```python
import asyncio
import helo

async def main():
    async with sdk_helo_email.AsyncHelo() as client:
        response = await client.sending.transactional(
            from_={"email": "sender@example.com"},
            to=[{"email": "user@example.com"}],
            subject="Hello",
            text="Hi!",
        )
        print(response.message_id)

asyncio.run(main())
```

## Automatic Retries

Requests that fail with a transient error — connection errors, timeouts, `429`,
and `5xx` responses — are retried automatically with exponential backoff. When the
server sends a `Retry-After` header (such as on a `429`), it is honored. Control
the number of retries with `max_retries` (set to `0` to disable):

```python
client = sdk_helo_email.Helo(max_retries=5)
```

## Sending

### Transactional email

```python
response = client.sending.transactional(
    from_={"email": "sender@example.com"},
    to=[{"email": "user@example.com"}],
    subject="Your order shipped",
    html="<p>Your order is on its way.</p>",
    text="Your order is on its way.",
    # Optional
    cc=[{"email": "support@example.com"}],
    bcc=[{"email": "archive@example.com"}],
    reply_to=[{"email": "noreply@example.com"}],
    tags=["order", "shipping"],
    metadata={"order_id": "12345"},
    channel_id="ch_abc123",
    idempotency_key="order-12345-shipped",
)
```

### Transactional batch

```python
response = client.sending.transactional_batch(
    requests=[
        {
            "from": {"email": "sender@example.com"},
            "to": [{"email": "user1@example.com"}],
            "subject": "Hello Alice",
            "text": "Hi Alice!",
        },
        {
            "from": {"email": "sender@example.com"},
            "to": [{"email": "user2@example.com"}],
            "subject": "Hello Bob",
            "text": "Hi Bob!",
        },
    ],
    channel_id="ch_abc123",
)
```

### Broadcast (template-driven, multi-recipient)

```python
response = client.sending.broadcast(
    from_={"email": "newsletter@example.com"},
    template={"id": "tmpl_abc123"},
    messages=[
        {"to": [{"email": "user1@example.com"}], "variables": {"name": "Alice"}},
        {"to": [{"email": "user2@example.com"}], "variables": {"name": "Bob"}},
    ],
    channel_id="ch_abc123",
)
```

### Broadcast message (single recipient)

```python
response = client.sending.broadcast_message(
    from_={"email": "newsletter@example.com"},
    to=[{"email": "user@example.com"}],
    subject="This month's digest",
    html="<p>Here's what's new...</p>",
    channel_id="ch_abc123",
)
```

## Channels

```python
# Create
channel = client.channels.create(
    name="Production",
    delivery_type=sdk_helo_email.DeliveryType.LIVE,
)

# List
channels = client.channels.list(limit=20, offset=0)

# Retrieve
channel = client.channels.retrieve("ch_abc123")

# Update
channel = client.channels.update("ch_abc123", name="Production v2")

# Delete
client.channels.delete("ch_abc123")
```

**`DeliveryType` values:** `LIVE`, `SANDBOX`

## Activity

```python
# List events
events = client.activity.list_events(
    channel_id="ch_abc123",
    start_date="2024-01-01",
    end_date="2024-01-31",
    event_types=[sdk_helo_email.EventType.DELIVERED, sdk_helo_email.EventType.OPENED],
    limit=50,
)

# List messages
messages = client.activity.list_messages(
    channel_id="ch_abc123",
    recipient="user@example.com",
    limit=25,
)

# Retrieve a message
message = client.activity.retrieve_message("msg_abc123")
```

**`EventType` values:** `DELIVERED`, `OPENED`, `CLICKED`, `BOUNCED`, `COMPLAINED`, `UNSUBSCRIBED`

**`MailType` values:** `TRANSACTIONAL`, `BROADCAST`

## Domains

```python
# Create
domain = client.domains.create(name="mail.example.com", channel_ids=["ch_abc123"])

# List
domains = client.domains.list(limit=10)

# Retrieve
domain = client.domains.retrieve("dom_abc123")

# Update (assign/reassign channels)
domain = client.domains.update("dom_abc123", channel_ids=["ch_abc123", "ch_xyz456"])

# Verify DNS records
dns_records = client.domains.verify("dom_abc123")

# Rotate DKIM key
dns_record = client.domains.rotate_key("dom_abc123")

# Delete
client.domains.delete("dom_abc123")
```

## Broadcasts

```python
# List broadcasts for a channel
broadcasts = client.broadcasts.list(
    channel_id="ch_abc123",
    status=sdk_helo_email.BroadcastStatus.SENT,
)

# Retrieve
broadcast = client.broadcasts.retrieve("brd_abc123")

# List delivery failures
failures = client.broadcasts.list_failures("brd_abc123")

# List suppressions generated by this broadcast
suppressions = client.broadcasts.list_suppressions("brd_abc123")
```

**`BroadcastStatus` values:** `PENDING`, `SENDING`, `SENT`, `FAILED`

## Statistics

```python
# Totals for a date range
totals = client.statistics.retrieve_totals(
    from_="2024-01-01",
    to="2024-01-31",
    channel_id="ch_abc123",
)

# Daily breakdown (timezone required)
daily = client.statistics.retrieve_daily(
    from_="2024-01-01",
    to="2024-01-31",
    timezone="America/New_York",
    channel_id="ch_abc123",
)

# Hourly breakdown
hourly = client.statistics.retrieve_hourly(
    from_="2024-01-15T00:00:00Z",
    to="2024-01-15T23:59:59Z",
    channel_id="ch_abc123",
)
```

## Suppressions

```python
# List
suppressions = client.suppressions.list(
    channel_id="ch_abc123",
    mail_type=sdk_helo_email.MailType.TRANSACTIONAL,
    reason=sdk_helo_email.SuppressionReason.BOUNCED,
)

# Add suppressions
result = client.suppressions.create(
    channel_id="ch_abc123",
    mail_type=sdk_helo_email.MailType.TRANSACTIONAL,
    emails=["bad@example.com", "invalid@example.com"],
)

# Remove suppressions
result = client.suppressions.remove(
    channel_id="ch_abc123",
    mail_type=sdk_helo_email.MailType.TRANSACTIONAL,
    emails=["reactivated@example.com"],
)
```

**`SuppressionReason` values:** `BOUNCED`, `COMPLAINED`, `UNSUBSCRIBED`, `MANUAL`

## Webhook Endpoints

```python
# Create
endpoint = client.webhook_endpoints.create(
    url="https://example.com/webhooks/helo",
    events=[sdk_helo_email.WebhookEvent.DELIVERED, sdk_helo_email.WebhookEvent.BOUNCED],
    channel_id="ch_abc123",
)

# List
endpoints = client.webhook_endpoints.list(channel_ids=["ch_abc123"])

# Retrieve
endpoint = client.webhook_endpoints.retrieve("whe_abc123")

# Update
endpoint = client.webhook_endpoints.update(
    "whe_abc123",
    enabled=False,
)

# Regenerate signing key
endpoint = client.webhook_endpoints.regenerate_signing_key("whe_abc123")

# Delete
client.webhook_endpoints.delete("whe_abc123")
```

**`WebhookEvent` values:** `DELIVERED`, `OPENED`, `CLICKED`, `BOUNCED`, `COMPLAINED`, `UNSUBSCRIBED`

## Error Handling

All API errors raise exceptions from the `helo` namespace:

```python
import helo

try:
    client.sending.transactional(
        from_={"email": "sender@example.com"},
        to=[{"email": "user@example.com"}],
        subject="Test",
    )
except sdk_helo_email.AuthenticationError as e:
    print(f"Auth failed: {e} (status {e.status_code})")
except sdk_helo_email.BadRequestError as e:
    print(f"Bad request: {e.detail}")
except sdk_helo_email.NotFoundError:
    print("Resource not found")
except sdk_helo_email.APIError as e:
    # Catch-all for any other API error
    print(f"API error {e.status_code}: {e}")
```

| Exception | HTTP Status |
|-----------|-------------|
| `BadRequestError` | 400 |
| `AuthenticationError` | 401 |
| `PermissionDeniedError` | 403 |
| `NotFoundError` | 404 |
| `ConflictError` | 409 |
| `UnprocessableEntityError` | 422 |
| `RateLimitError` | 429 |
| `InternalServerError` | 5xx |

All API errors subclass `APIError` and expose `.status_code`, `.error_code`, `.detail`,
and `.request_id`. `RateLimitError` additionally exposes `.retry_after` (seconds, when
the server provides it).

Network-level failures (after retries are exhausted) raise `APIConnectionError`, or
`APITimeoutError` for timeouts. Both subclass `HeloError` — the base class for every
exception this library raises — so `except sdk_helo_email.HeloError` catches everything.

## Development

Install the dev dependencies and run the checks:

```bash
pip install -e ".[dev]"
ruff check .
mypy helo
pytest
```

### Tests

The default `pytest` run uses mocked HTTP responses — it's fast, needs no
credentials, and is what the main CI workflow runs.

Integration tests (marked `@pytest.mark.integration`) exercise the **full** API
surface — creating, mutating, and deleting real resources, sending messages, and
reading back activity and statistics — and are **skipped by default**. They
target a local instance at `http://localhost:8000` by default and need an API
key. Run them with the `--integration` flag:

```bash
export HELO_API_KEY="your-api-key"
# Optionally point at a different environment (default: http://localhost:8000):
# export HELO_BASE_URL="https://staging.api.helohq.com"
pytest --integration
```

Created resources use unique names and are cleaned up automatically. Without
`HELO_API_KEY` set, the integration tests skip.

In CI they run via a separate, manually-triggered `Integration` workflow, so
pushes and PRs stay fast. Point it at a reachable API by setting the
`HELO_BASE_URL` repository variable and the `HELO_API_KEY` secret.
