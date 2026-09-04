# Webhooks

Create and manage webhooks for event notifications.

| Method | HTTP request | Description |
| ------ | ------------ | ----------- |
| [**webhooks.list**](#list) | **GET** /webhooks | List all webhooks |
| [**webhooks.create**](#create) | **POST** /webhooks | Create a webhook |
| [**webhooks.retrieve**](#retrieve) | **GET** /webhooks/{id} | Retrieve a webhook |
| [**webhooks.update**](#update) | **PATCH** /webhooks/{id} | Update a webhook |
| [**webhooks.delete**](#delete) | **DELETE** /webhooks/{id} | Delete a webhook |
| [**webhooks.regenerate_signing_key**](#regenerate_signing_key) | **POST** /webhooks/{id}/regenerate-signing-key | Regenerate webhook signing key |

## list

`GET /webhooks`

Retrieves all webhooks configured for the account.

```python Webhooks_list
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

pagination_result_of_webhook = client.webhooks.list(limit=10, offset=10)
```

## create

`POST /webhooks`

Registers a new webhook to receive event notifications.

```python Webhooks_create
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

webhook = client.webhooks.create(
    url="test-url",
    events=[helo.WebhookEvent.MESSAGE_ACCEPTED],
    channel_id="550e8400-e29b-41d4-a716-446655440000",
    additional_headers=[{"name": "test-name", "value": "test-value"}],
    enabled=True,
)
```

## retrieve

`GET /webhooks/{id}`

Fetches the details and configuration of a specific webhook.

```python Webhooks_retrieve
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

webhook = client.webhooks.retrieve("550e8400-e29b-41d4-a716-446655440000")
```

## update

`PATCH /webhooks/{id}`

Modifies an existing webhook by ID.

```python Webhooks_update
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

webhook = client.webhooks.update(
    "550e8400-e29b-41d4-a716-446655440000",
    url="test-url",
    events=[helo.WebhookEvent.MESSAGE_ACCEPTED],
    channel_id="550e8400-e29b-41d4-a716-446655440000",
    additional_headers=[{"name": "test-name", "value": "test-value"}],
    enabled=True,
)
```

## delete

`DELETE /webhooks/{id}`

Permanently removes a webhook.

```python Webhooks_delete
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

client.webhooks.delete("550e8400-e29b-41d4-a716-446655440000")
```

## regenerate_signing_key

`POST /webhooks/{id}/regenerate-signing-key`

Regenerate the signing key used for the webhook signature. This operation replaces the old key.

```python Webhooks_regenerateSigningKey
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

webhook = client.webhooks.regenerate_signing_key("550e8400-e29b-41d4-a716-446655440000")
```
