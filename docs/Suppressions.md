# Suppressions

Manage suppressed recipients.

## List suppressions

`GET /suppressions`

```python Suppressions_list
import sdk_helo_email as helo

client = helo.Helo(api_key="your-api-key")

suppressions = client.suppressions.list(
    channel_id="channel-id",
    mail_type=helo.MailType.TRANSACTIONAL,
)
```

## Add suppressions

`POST /suppressions`

```python Suppressions_create
import sdk_helo_email as helo

client = helo.Helo(api_key="your-api-key")

result = client.suppressions.create(
    channel_id="channel-id",
    mail_type=helo.MailType.TRANSACTIONAL,
    emails=["blocked@example.com"],
)
```

## Remove suppressions

`POST /suppressions/remove`

```python Suppressions_remove
import sdk_helo_email as helo

client = helo.Helo(api_key="your-api-key")

result = client.suppressions.remove(
    channel_id="channel-id",
    mail_type=helo.MailType.TRANSACTIONAL,
    emails=["blocked@example.com"],
)
```
