# Changelog

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
