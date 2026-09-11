# Sending

Send transactional and broadcast emails.

| Method | HTTP request | Description |
| ------ | ------------ | ----------- |
| [**sending.send_transactional**](#send_transactional) | **POST** /send/transactional | Send a transactional email |
| [**sending.send_transactional_batch**](#send_transactional_batch) | **POST** /send/transactional/batch | Send transactional emails in batch |
| [**sending.send_broadcast**](#send_broadcast) | **POST** /send/broadcast |  |
| [**sending.send_broadcast_message**](#send_broadcast_message) | **POST** /send/broadcast/message | Send a single broadcast email |

## send_transactional

`POST /send/transactional`

Sends a single transactional email such as receipts, confirmations, or notifications.

```python Sending_sendTransactional
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

send_message_accepted = client.sending.send_transactional(
    from_={"email": "from@yourdomain.com", "name": "From name"},
    to=[{"email": "to@example.com", "name": "To name"}],
    cc=[{"email": "cc@example.com", "name": "Cc name"}],
    bcc=[{"email": "bcc@example.com", "name": "Bcc name"}],
    reply_to=[{"email": "reply-to@example.com", "name": "Reply-To name"}],
    subject="Hello from Helo",
    html="<html><body><h1>Hi there, new friend.</h1><p>This is a test message, delivered with <3 by Helo. </p></body></html>",
    text="This is a test message, delivered with <3 by Helo.",
    template={
        "subject": "test-subject",
        "html": "test-html",
        "text": "test-text",
        "inlineStyles": True,
    },
    tracking={"opens": True, "links": True},
    attachments=[
        {
            "content": "SGVsbG8gd29ybGQ=",
            "contentId": "test-contentId",
            "contentType": "test-contentType",
            "fileName": "test-fileName",
            "disposition": helo.AttachmentDisposition.ATTACHMENT,
        },
    ],
    tags=["welcome", "onboarding"],
    channel_id="550e8400-e29b-41d4-a716-446655440000",
    idempotency_key="test-idempotency_key",
)
```

## send_transactional_batch

`POST /send/transactional/batch`

Sends multiple transactional emails in a single API request for better performance.

```python Sending_sendTransactionalBatch
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

send_message_batch = client.sending.send_transactional_batch(
    requests=[
        {
            "from": {"email": "from@yourdomain.com", "name": "From name"},
            "to": [{"email": "to@example.com", "name": "To name"}],
            "subject": "Hello from Helo",
            "html": "<html><body><h1>Hi there, new friend.</h1><p>This is a test message, delivered with <3 by Helo. </p></body></html>",
            "text": "This is a test message, delivered with <3 by Helo.",
            "tags": ["welcome", "onboarding"],
        },
    ],
    channel_id="550e8400-e29b-41d4-a716-446655440000",
    idempotency_key="test-idempotency_key",
)
```

## send_broadcast

`POST /send/broadcast`

```python Sending_sendBroadcast
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

send_broadcast = client.sending.send_broadcast(
    from_={"email": "test@example.com", "name": "test-name"},
    template={
        "subject": "test-subject",
        "html": "test-html",
        "text": "test-text",
        "inlineStyles": True,
    },
    messages=[
        {
            "to": [{"email": "test@example.com", "name": "test-name"}],
            "tags": ["test-tag"],
        },
    ],
    reply_to=[{"email": "test@example.com", "name": "test-name"}],
    tracking={"opens": True, "links": True},
    attachments=[
        {
            "content": "SGVsbG8gd29ybGQ=",
            "contentId": "test-contentId",
            "contentType": "test-contentType",
            "fileName": "test-fileName",
            "disposition": helo.AttachmentDisposition.ATTACHMENT,
        },
    ],
    tags=["test-tag"],
    channel_id="550e8400-e29b-41d4-a716-446655440000",
    idempotency_key="test-idempotency_key",
)
```

## send_broadcast_message

`POST /send/broadcast/message`

Sends a single broadcast email message.

```python Sending_sendBroadcastMessage
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

send_message_accepted = client.sending.send_broadcast_message(
    from_={"email": "from@yourdomain.com", "name": "From name"},
    to=[{"email": "to@example.com", "name": "To name"}],
    cc=[{"email": "cc@example.com", "name": "Cc name"}],
    bcc=[{"email": "bcc@example.com", "name": "Bcc name"}],
    reply_to=[{"email": "reply-to@example.com", "name": "Reply-To name"}],
    subject="Hello from Helo",
    html="<html><body><h1>Hi there, new friend.</h1><p>This is a test message, delivered with <3 by Helo. </p></body></html>",
    text="This is a test message, delivered with <3 by Helo.",
    template={
        "subject": "test-subject",
        "html": "test-html",
        "text": "test-text",
        "inlineStyles": True,
    },
    tracking={"opens": True, "links": True},
    attachments=[
        {
            "content": "SGVsbG8gd29ybGQ=",
            "contentId": "test-contentId",
            "contentType": "test-contentType",
            "fileName": "test-fileName",
            "disposition": helo.AttachmentDisposition.ATTACHMENT,
        },
    ],
    tags=["welcome", "onboarding"],
    channel_id="550e8400-e29b-41d4-a716-446655440000",
    idempotency_key="test-idempotency_key",
)
```
