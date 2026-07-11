# Webhooks

Manage webhook endpoints. In the Python SDK these live under `client.webhook_endpoints`.

## Create a webhook endpoint

`POST /webhooks`

```python Webhooks_create
import sdk_helo_email as helo

client = helo.Helo(api_key="your-api-key")

webhook = client.webhook_endpoints.create(
    url="https://example.com/webhooks/helo",
    events=[helo.WebhookEvent.DELIVERED, helo.WebhookEvent.BOUNCED],
    channel_id="channel-id",
    enabled=True,
)
```

## List webhook endpoints

`GET /webhooks`

```python Webhooks_list
import sdk_helo_email as helo

client = helo.Helo(api_key="your-api-key")

webhooks = client.webhook_endpoints.list(limit=20)
```

## Retrieve a webhook endpoint

`GET /webhooks/{id}`

```python Webhooks_retrieve
import sdk_helo_email as helo

client = helo.Helo(api_key="your-api-key")

webhook = client.webhook_endpoints.retrieve("webhook-id")
```

## Update a webhook endpoint

`PATCH /webhooks/{id}`

```python Webhooks_update
import sdk_helo_email as helo

client = helo.Helo(api_key="your-api-key")

webhook = client.webhook_endpoints.update("webhook-id", enabled=False)
```

## Delete a webhook endpoint

`DELETE /webhooks/{id}`

```python Webhooks_delete
import sdk_helo_email as helo

client = helo.Helo(api_key="your-api-key")

client.webhook_endpoints.delete("webhook-id")
```

## Regenerate a webhook signing key

`POST /webhooks/{id}/regenerate-signing-key`

```python Webhooks_regenerateSigningKey
import sdk_helo_email as helo

client = helo.Helo(api_key="your-api-key")

webhook = client.webhook_endpoints.regenerate_signing_key("webhook-id")
```
