# Channels

Create and manage communication channels for organizing messages.

| Method | HTTP request | Description |
| ------ | ------------ | ----------- |
| [**channels.list**](#list) | **GET** /channels | List all channels |
| [**channels.create**](#create) | **POST** /channels | Create a channel |
| [**channels.retrieve**](#retrieve) | **GET** /channels/{id} | Retrieve a channel |
| [**channels.update**](#update) | **PATCH** /channels/{id} | Update a channel |
| [**channels.delete**](#delete) | **DELETE** /channels/{id} | Delete a channel |

## list

`GET /channels`

Retrieves a list of all channels accessible to the current user.

```python Channels_list
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

pagination_result_of_channel_basic = client.channels.list(limit=10, offset=10)
```

## create

`POST /channels`

Creates a new communication channel for organizing and routing messages.

```python Channels_create
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

channel_details = client.channels.create(
    name="test-name",
    delivery_type=helo.DeliveryType.LIVE,
    tracking={"links": True, "opens": True},
)
```

## retrieve

`GET /channels/{id}`

Fetches the details and configuration of a specific channel.

```python Channels_retrieve
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

channel_details = client.channels.retrieve("550e8400-e29b-41d4-a716-446655440000")
```

## update

`PATCH /channels/{id}`

Modifies an existing channel by ID.

```python Channels_update
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

channel_details = client.channels.update(
    "550e8400-e29b-41d4-a716-446655440000",
    name="test-name",
    delivery_type=helo.DeliveryType.LIVE,
    tracking={"links": True, "opens": True},
)
```

## delete

`DELETE /channels/{id}`

Permanently removes a channel and all associated data.

```python Channels_delete
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

client.channels.delete("550e8400-e29b-41d4-a716-446655440000")
```
