# Suppressions

| Method | HTTP request | Description |
| ------ | ------------ | ----------- |
| [**suppressions.list**](#list) | **GET** /suppressions | List suppressions |
| [**suppressions.create**](#create) | **POST** /suppressions | Create suppressions |
| [**suppressions.remove**](#remove) | **POST** /suppressions/remove | Remove suppressions |

## list

`GET /suppressions`

Retrieves a list of suppressed email addresses for a channel.

```python Suppressions_list
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

paginated_response_of_suppression = client.suppressions.list(
    channel_id="550e8400-e29b-41d4-a716-446655440000",
    mail_type=helo.MailType.TRANSACTIONAL,
    reason=helo.SuppressionReason.BOUNCE,
    email="test@example.com",
)
```

## create

`POST /suppressions`

Adds email addresses to the suppression list to prevent future sends.

```python Suppressions_create
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

create_suppressions = client.suppressions.create(
    channel_id="550e8400-e29b-41d4-a716-446655440000",
    mail_type=helo.MailType.TRANSACTIONAL,
    emails=["test@example.com"],
)
```

## remove

`POST /suppressions/remove`

Removes email addresses from the suppression list to allow future sends.

```python Suppressions_remove
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

remove_suppressions = client.suppressions.remove(
    channel_id="550e8400-e29b-41d4-a716-446655440000",
    mail_type=helo.MailType.TRANSACTIONAL,
    emails=["test@example.com"],
)
```
