# Activity

Track and retrieve message activity, including messages, delivery and engagement events.

| Method | HTTP request | Description |
| ------ | ------------ | ----------- |
| [**activity.list_events**](#list_events) | **GET** /activity/events | List activity events |
| [**activity.list_messages**](#list_messages) | **GET** /activity/messages | List messages |
| [**activity.retrieve_message**](#retrieve_message) | **GET** /activity/messages/{id} | Retrieve message details |

## list_events

`GET /activity/events`

Retrieves activity events for messages, including delivery status, opens, clicks, bounces, unsubscribes and complaints.

```python Activity_listEvents
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

paginated_events = client.activity.list_events(
    channel_id="550e8400-e29b-41d4-a716-446655440000",
    message_id="550e8400-e29b-41d4-a716-446655440000",
)
```

## list_messages

`GET /activity/messages`

Retrieves a paginated list of sent messages with basic tracking information.

```python Activity_listMessages
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

paginated_messages = client.activity.list_messages(
    channel_id="550e8400-e29b-41d4-a716-446655440000",
    after=10,
)
```

## retrieve_message

`GET /activity/messages/{id}`

Fetches detailed tracking information for a specific message, including all associated events.

```python Activity_retrieveMessage
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

message_details = client.activity.retrieve_message(
    "550e8400-e29b-41d4-a716-446655440000",
)
```
