# Broadcasts

Query broadcast campaigns.

## List broadcasts

`GET /broadcasts`

```python Broadcasts_list
import sdk_helo_email as helo

client = helo.Helo(api_key="your-api-key")

broadcasts = client.broadcasts.list(
    channel_id="channel-id",
    status=helo.BroadcastStatus.COMPLETED,
)
```

## Retrieve a broadcast

`GET /broadcasts/{id}`

```python Broadcasts_retrieve
import sdk_helo_email as helo

client = helo.Helo(api_key="your-api-key")

broadcast = client.broadcasts.retrieve("broadcast-id")
```

## List a broadcast's failures

`GET /broadcasts/{id}/failures`

```python Broadcasts_listFailures
import sdk_helo_email as helo

client = helo.Helo(api_key="your-api-key")

failures = client.broadcasts.list_failures("broadcast-id")
```

## List a broadcast's suppressions

`GET /broadcasts/{id}/suppressions`

```python Broadcasts_listSuppressions
import sdk_helo_email as helo

client = helo.Helo(api_key="your-api-key")

suppressions = client.broadcasts.list_suppressions("broadcast-id")
```
