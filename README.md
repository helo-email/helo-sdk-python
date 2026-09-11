# Helo Python SDK

Helo Email API (https://helohq.com)

## Installation

```bash
pip install sdk_helo_email
```

Requires Python 3.10+ and installs `httpx` and `pydantic` automatically.

## Quick start

```python
import sdk_helo_email as helo

# The API key is read from HELO_API_KEY when not passed explicitly.
client = helo.Helo()

paginated_events = client.activity.list_events(
    channel_id="550e8400-e29b-41d4-a716-446655440000",
    message_id="550e8400-e29b-41d4-a716-446655440000",
)
```

Pass the key directly when you manage several accounts or read it from a secrets manager:

```python
client = helo.Helo(api_key="your-api-key")
```

Override the base URL, timeout, or retry count (defaults: `https://api.helohq.com`, 30 seconds,
2 retries):

```python
client = helo.Helo(
    base_url="https://api.helohq.com",
    timeout=60.0,
    max_retries=2,
)
```

Use `with` so the underlying connection pool is closed:

```python
with helo.Helo() as client:
    ...
```

## Async

`AsyncHelo` mirrors the synchronous API; every resource method becomes a coroutine.

```python
import asyncio
import sdk_helo_email as helo


async def main() -> None:
    async with helo.AsyncHelo() as client:
        paginated_events = await client.activity.list_events(
            channel_id="550e8400-e29b-41d4-a716-446655440000",
            message_id="550e8400-e29b-41d4-a716-446655440000",
        )


asyncio.run(main())
```

## Automatic retries

Connection errors, timeouts, `429`, and `5xx` responses are retried with exponential backoff and
full jitter. A `Retry-After` header is honoured when present. Set `max_retries=0` to disable.

## Resources

| Attribute | Documentation |
| --------- | ------------- |
| `client.activity` | [docs/Activity.md](docs/Activity.md) |
| `client.broadcasts` | [docs/Broadcasts.md](docs/Broadcasts.md) |
| `client.channels` | [docs/Channels.md](docs/Channels.md) |
| `client.domains` | [docs/Domains.md](docs/Domains.md) |
| `client.sending` | [docs/Sending.md](docs/Sending.md) |
| `client.statistics` | [docs/Statistics.md](docs/Statistics.md) |
| `client.suppressions` | [docs/Suppressions.md](docs/Suppressions.md) |
| `client.webhooks` | [docs/Webhooks.md](docs/Webhooks.md) |

## Error handling

Every API error subclasses `APIError` and carries `.status_code`, `.error_code`, `.detail`, and
`.request_id`. `RateLimitError` also exposes `.retry_after`.

```python
import sdk_helo_email as helo

try:
    paginated_events = client.activity.list_events(
except helo.AuthenticationError as exc:
    print(f"auth failed: {exc} (status {exc.status_code})")
except helo.APIError as exc:
    print(f"API error {exc.status_code}: {exc}")
```

| Exception | HTTP status |
| --------- | ----------- |
| `BadRequestError` | 400 |
| `AuthenticationError` | 401 |
| `PermissionDeniedError` | 403 |
| `NotFoundError` | 404 |
| `ConflictError` | 409 |
| `UnprocessableEntityError` | 422 |
| `RateLimitError` | 429 |
| `InternalServerError` | 5xx |

Network failures raise `APIConnectionError` (or `APITimeoutError`) once retries are exhausted.
Both subclass `HeloError`, the base of every exception this library raises.

## Webhook signature verification

Webhook deliveries are signed with the endpoint's signing key. Verify every delivery before
acting on it, against the **raw** request body — parsing and re-serializing the JSON changes
the bytes and the signature will not match.

```python
import json
import os

from flask import Flask, abort, request

import sdk_helo_email as helo

app = Flask(__name__)


@app.post("/webhooks/helo")
def receive_webhook() -> tuple[str, int]:
    try:
        helo.verify_webhook_signature(
            request.headers.get("X-Helo-Webhook-Signature"),
            request.get_data(),  # raw body, exactly as received
            os.environ["HELO_WEBHOOK_SIGNING_KEY"],
        )
    except helo.WebhookSignatureError:
        abort(400)

    event = json.loads(request.get_data())
    # ... handle the event, then acknowledge quickly
    return "", 204
```

`verify_webhook_signature` returns `None` when the signature is valid and raises otherwise.
Each rejection has its own class, so a stale delivery can be treated differently from a
genuinely bad one:

| Exception | Meaning |
| --- | --- |
| `WebhookSignatureMalformedHeaderError` | The header was not in the expected format |
| `WebhookSignatureUnsupportedVersionError` | The delivery used a signing scheme this SDK version cannot verify — upgrade the package |
| `WebhookSignatureTimestampSkewError` | Correctly signed, but too old to accept — possible replay, or clock drift |
| `WebhookSignatureMismatchError` | Wrong signing key, or the body was modified in transit |

All four inherit from `WebhookSignatureError` (itself a `HeloError`), so catch that
one class to handle any rejection. If you only want a boolean, use
`is_valid_webhook_signature` instead:

```python
if helo.is_valid_webhook_signature(signature_header, raw_body, signing_key):
    ...
```

The body may be passed as `str` or `bytes`. The signature header may carry several versions at
once (`t=...,v1=...,v2=...`) while a new signing scheme is being rolled out. This SDK verifies
against the newest version it supports (`SUPPORTED_WEBHOOK_SIGNATURE_VERSIONS`) and ignores
elements it does not recognize, so a rollout will not break this integration.

To compute a signature yourself — signing a fixture in tests, for example — use
`generate_webhook_signature(payload, signing_key, timestamp)`.

## Development

```bash
make install
make check
make test
```
