# Sending

Send transactional and broadcast emails through the Helo API.

## Send a transactional email

`POST /send/transactional`

```python Sending_transactional
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

response = client.sending.transactional(
    from_={"email": "from@yourdomain.com", "name": "From name"},
    to=[{"email": "to@example.com"}],
    subject="Hello from Helo",
    html="<html><body><h1>Hi there, new friend.</h1><p>This is a test message, delivered with <3 by Helo. </p></body></html>",
    text="This is a test message, delivered with <3 by Helo.",
    tags=["welcome", "onboarding"],
    channel_id="your-channel-id",
)
```

## Send transactional emails in batch

`POST /send/transactional/batch`

```python Sending_transactionalBatch
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

response = client.sending.transactional_batch(
    requests=[
        {
            "from": {"email": "from@yourdomain.com", "name": "From name"},
            "to": [{"email": "first@example.com"}],
            "subject": "Hello from Helo",
            "html": "<html><body><h1>Hi there, new friend.</h1><p>This is a test message, delivered with <3 by Helo. </p></body></html>",
            "text": "This is a test message, delivered with <3 by Helo."
        },
        {
            "from": {"email": "from@yourdomain.com", "name": "From name"},
            "to": [{"email": "second@example.com"}],
            "subject": "Hello from Helo",
            "html": "<html><body><h1>Hi there, new friend.</h1><p>This is a test message, delivered with <3 by Helo. </p></body></html>",
            "text": "This is a test message, delivered with <3 by Helo."
        }
    ],
    channel_id="your-channel-id",
)
```

## Send a broadcast email

`POST /send/broadcast`

```python Sending_broadcast
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

response = client.sending.broadcast(
    from_={"email": "from@yourdomain.com", "name": "From name"},
    template={"subject": "Product update", "html": "<p>Here's what's new this month.</p>"},
    messages=[
        {"to": [{"email": "first@example.com"}]},
        {"to": [{"email": "second@example.com"}]},
    ],
    channel_id="your-channel-id",
)
```

## Send a single broadcast email

`POST /send/broadcast/message`

```python Sending_broadcastMessage
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

response = client.sending.broadcast_message(
    from_={"email": "from@yourdomain.com", "name": "From name"},
    to=[{"email": "to@example.com"}],
    subject="Hello from Helo",
    html="<html><body><h1>Hi there, new friend.</h1><p>This is a test message, delivered with <3 by Helo. </p></body></html>",
    channel_id="your-channel-id",
)
```
