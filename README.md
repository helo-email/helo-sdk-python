# Helo Python SDK

Helo API

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

## Development

```bash
make install
make check
make test
```
