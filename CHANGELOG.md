# Changelog

## 1.4.0

- Fixed `send_transactional`, `send_transactional_batch`, `send_broadcast` and
  `send_broadcast_message` sending each recipient, attachment, batched request and broadcast
  message as a string (`"{'email': ...}"`) instead of an object. `webhooks.update` and
  `webhooks.create` had the same problem with `additional_headers`.
- Fixed retries repeating requests that could be acted on twice: a `POST` without an
  idempotency key is no longer retried after a network error or a `5xx`. A `Retry-After` of more
  than 8 seconds is now returned as the error rather than retried early.
- `send_transactional`, `send_transactional_batch`, `send_broadcast` and
  `send_broadcast_message` now generate an idempotency key when you don't pass
  `idempotency_key`, and send the same key on every retry, so a send whose response was lost is
  never sent twice.
- Added `null_fields` to `templates.update` and `webhooks.update`, to clear a field:
  `client.templates.update(template_id, null_fields=["text"])`.
- An enum value added to the API after this release no longer fails to parse; it becomes a new
  member of the enum, holding the value.

## 1.3.0

- Added sending template management
- Added support for custom tracking domains

## 1.2.0

- Dropped support for Python 3.10, which reached end of life in October 2026; the SDK now requires
  Python 3.11 or later. pip won't install this version on 3.10, which keeps the previous one.
- Added Python 3.14 to the versions the SDK is tested on.

## 1.1.0

- Added `id` to the `template` of transactional and broadcast send requests, to send a stored template
  instead of an inline `subject`, `html` and `text`.

## 1.0.1

- Release pipeline updates

## 1.0.0

- Initial release
