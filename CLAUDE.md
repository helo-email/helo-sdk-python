# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this
repository.

## This repository is generated

Every file here except `.git` is produced by the `helo-sdk-generator-python` gem, which lives in
the `helo-sdk-generator` repo (checked out next to this one) under
`vendor/gems/helo-sdk-generator-python`. Regenerating sweeps the working tree first, so **any edit
made here is lost on the next run**. Fix the generator's Ruby or ERB templates instead, then
regenerate:

```bash
cd ../helo-sdk-generator && ./exe/helo-sdk-generator public
```

## Commands

```bash
make install            # pip install -e ".[dev]"
make check              # ruff check . && mypy sdk_helo_email
make test               # pytest (mocked HTTP, no server needed)
make build              # build a wheel and sdist
```

## Architecture

- `Helo` / `AsyncHelo` (`_client.py`) — the two facades. Each exposes one
  resource per API tag and resolves the API key from `HELO_API_KEY` when not passed.
- `resources/<tag>.py` — a sync and an async resource class per tag, generated from the same
  operation list so the two stay in step.
- `_http.py` — httpx transport, retries with jittered backoff (honouring `Retry-After`), and the
  status-code-to-exception mapping. `_exceptions.py` holds that hierarchy.
- `types/shared.py` — the `HeloModel` pydantic base plus every enum. `types/<tag>.py` holds
  the response models a single tag owns; models two or more tags reach live in `shared`.
- `types/params.py` — TypedDicts for the object-shaped values request bodies accept.

Request bodies are flattened into keyword arguments, so callers write
`client.sending.transactional(from_=..., to=[...])` rather than assembling a dict. `_utils.py`
converts those snake_case names to the API's camelCase and drops the ones left as `None`.

## Documentation & code samples

`docs/*.md` holds one file per tag. Each example is a fenced block whose info string is the
operation's OpenAPI `operationId`:

    ```python Activity_listEvents
    ...
    ```

`helo-sdk-generator` extracts those blocks and embeds them into the published OpenAPI description
as the Python `x-codeSamples` entry for that operation, so the info string must stay an exact
`operationId`.
