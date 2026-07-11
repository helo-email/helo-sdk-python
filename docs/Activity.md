# Activity

Query message activity and events.

## List events

`GET /activity/events`

```python Activity_listEvents
import sdk_helo_email as helo

client = helo.Helo(api_key="your-api-key")

events = client.activity.list_events(start_date="2024-01-01", limit=50)
```

## List messages

`GET /activity/messages`

```python Activity_listMessages
import sdk_helo_email as helo

client = helo.Helo(api_key="your-api-key")

messages = client.activity.list_messages(recipient="customer@example.com", limit=50)
```

## Retrieve a message

`GET /activity/messages/{id}`

```python Activity_retrieveMessage
import sdk_helo_email as helo

client = helo.Helo(api_key="your-api-key")

message = client.activity.retrieve_message("message-id")
```
