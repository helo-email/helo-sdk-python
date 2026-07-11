# Domains

Manage sending domains and their DNS records.

## Create a domain

`POST /domains`

```python Domains_create
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

domain = client.domains.create(name="mail.example.com", channel_ids=["channel-id"])
```

## List domains

`GET /domains`

```python Domains_list
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

domains = client.domains.list(limit=20)
```

## Retrieve a domain

`GET /domains/{id}`

```python Domains_retrieve
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

domain = client.domains.retrieve("domain-id")
```

## Update a domain

`PATCH /domains/{id}`

```python Domains_update
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

domain = client.domains.update("domain-id", channel_ids=["channel-id"])
```

## Delete a domain

`DELETE /domains/{id}`

```python Domains_delete
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

client.domains.delete("domain-id")
```

## Verify a domain

`POST /domains/{id}/verify`

```python Domains_verify
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

dns_records = client.domains.verify("domain-id")
```

## Rotate a domain's DKIM key

`POST /domains/{id}/rotate-key`

```python Domains_rotateKey
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

dns_record = client.domains.rotate_key("domain-id")
```
