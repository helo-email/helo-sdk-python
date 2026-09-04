# Domains

Register, verify, and manage domains for email sending.

| Method | HTTP request | Description |
| ------ | ------------ | ----------- |
| [**domains.list**](#list) | **GET** /domains | List all domains |
| [**domains.create**](#create) | **POST** /domains | Create a domain |
| [**domains.retrieve**](#retrieve) | **GET** /domains/{id} | Retrieve a domain |
| [**domains.update**](#update) | **PATCH** /domains/{id} | Update a domain |
| [**domains.delete**](#delete) | **DELETE** /domains/{id} | Delete a domain |
| [**domains.verify**](#verify) | **POST** /domains/{id}/verify | Verify a domain |
| [**domains.rotate_key**](#rotate_key) | **POST** /domains/{id}/rotate-key | Rotate a domain key |

## list

`GET /domains`

Retrieves all domains associated with the current account, including their verification status.

```python Domains_list
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

paginated_response_of_domain = client.domains.list(limit=10, offset=10)
```

## create

`POST /domains`

Registers a new domain for sending emails. The domain must be verified before it can be used.

```python Domains_create
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

domain_with_dns = client.domains.create(
    name="test-name",
    channel_ids=["550e8400-e29b-41d4-a716-446655440000"],
)
```

## retrieve

`GET /domains/{id}`

Gets detailed information about a specific domain, including verification status and configuration.

```python Domains_retrieve
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

domain_with_dns = client.domains.retrieve("550e8400-e29b-41d4-a716-446655440000")
```

## update

`PATCH /domains/{id}`

Modifies an existing domain by ID.

```python Domains_update
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

domain = client.domains.update(
    "550e8400-e29b-41d4-a716-446655440000",
    channel_ids=["550e8400-e29b-41d4-a716-446655440000"],
)
```

## delete

`DELETE /domains/{id}`

Removes a domain from the account. This will stop all email sending from this domain.

```python Domains_delete
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

client.domains.delete("550e8400-e29b-41d4-a716-446655440000")
```

## verify

`POST /domains/{id}/verify`

Initiates the domain verification process by checking DNS records.

```python Domains_verify
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

dns_records = client.domains.verify("550e8400-e29b-41d4-a716-446655440000")
```

## rotate_key

`POST /domains/{id}/rotate-key`

Generates new DKIM keys for the domain. This is recommended for security best practices.

```python Domains_rotateKey
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

dns_record = client.domains.rotate_key("550e8400-e29b-41d4-a716-446655440000")
```
