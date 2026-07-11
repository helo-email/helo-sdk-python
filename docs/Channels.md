# Channels

Manage sending channels.

## Create a channel

`POST /channels`

```python Channels_create
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

channel = client.channels.create(
    name="Transactional",
    delivery_type=helo.DeliveryType.LIVE,
    tracking={"links": True, "opens": True},
)
```

## List channels

`GET /channels`

```python Channels_list
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

channels = client.channels.list(limit=20, delivery_type=helo.DeliveryType.LIVE)
```

## Retrieve a channel

`GET /channels/{id}`

```python Channels_retrieve
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

channel = client.channels.retrieve("channel-id")
```

## Update a channel

`PATCH /channels/{id}`

```python Channels_update
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

channel = client.channels.update("channel-id", name="Marketing")
```

## Delete a channel

`DELETE /channels/{id}`

```python Channels_delete
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

client.channels.delete("channel-id")
```
