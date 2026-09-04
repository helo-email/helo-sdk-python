# Broadcasts

Manage and track broadcast email campaigns.

| Method | HTTP request | Description |
| ------ | ------------ | ----------- |
| [**broadcasts.list**](#list) | **GET** /broadcasts | List broadcasts |
| [**broadcasts.retrieve**](#retrieve) | **GET** /broadcasts/{id} | Retrieve a broadcast |
| [**broadcasts.list_failures**](#list_failures) | **GET** /broadcasts/{id}/failures | List failed broadcast messages |
| [**broadcasts.list_suppressions**](#list_suppressions) | **GET** /broadcasts/{id}/suppressions | List broadcast suppressed recipients |

## list

`GET /broadcasts`

Retrieves a paginated list of sent broadcasts with summary statistics.

```python Broadcasts_list
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

paginated_response_of_broadcast = client.broadcasts.list(
    channel_id="550e8400-e29b-41d4-a716-446655440000",
    status=helo.BroadcastStatus.ACCEPTED,
    subject="test-subject",
)
```

## retrieve

`GET /broadcasts/{id}`

Fetches details and statistics for a specific broadcast.

```python Broadcasts_retrieve
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

broadcast_details = client.broadcasts.retrieve("550e8400-e29b-41d4-a716-446655440000")
```

## list_failures

`GET /broadcasts/{id}/failures`

Returns messages that could not be delivered due to permanent errors (e.g. invalid addresses, domain issues). Transient errors that were retried successfully do not appear here.

```python Broadcasts_listFailures
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

paginated_response_of_broadcast_failure = client.broadcasts.list_failures(
    "550e8400-e29b-41d4-a716-446655440000",
    limit=10,
    offset=10,
)
```

## list_suppressions

`GET /broadcasts/{id}/suppressions`

Returns recipients that were skipped because they appear on a suppression list (e.g. previous bounces or unsubscribes).

```python Broadcasts_listSuppressions
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

paginated_response_of_broadcast_suppression = client.broadcasts.list_suppressions(
    "550e8400-e29b-41d4-a716-446655440000",
    limit=10,
    offset=10,
)
```
