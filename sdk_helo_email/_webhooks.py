"""Helpers for verifying the signature on an incoming webhook request."""

from __future__ import annotations

import hashlib
import hmac
import re
import time

from ._exceptions import (
    WebhookSignatureError,
    WebhookSignatureMalformedHeaderError,
    WebhookSignatureMismatchError,
    WebhookSignatureTimestampSkewError,
    WebhookSignatureUnsupportedVersionError,
)

# Signing schemes this SDK can verify. The signature header may carry several
# versions at once (``t=...,v1=...,v2=...``) so that a new scheme can be rolled
# out while receivers upgrade; verification uses the newest version present that
# appears in this tuple, and ignores the rest.
SUPPORTED_WEBHOOK_SIGNATURE_VERSIONS: tuple[int, ...] = (1,)

# How far a signature's timestamp may be from the current time, in seconds,
# before it is rejected.
MAX_WEBHOOK_TIMESTAMP_SKEW_SECONDS = 300  # 5 minutes

_TIMESTAMP_VALUE_REGEX = re.compile(r"\A\d+\Z")
_SIGNATURE_KEY_REGEX = re.compile(r"\Av(\d+)\Z")
_HEX_SIGNATURE_REGEX = re.compile(r"\A[a-f0-9]+\Z")


def verify_webhook_signature(
    signature_header: str | None, request_body: str | bytes, signing_key: str
) -> None:
    """Verify a webhook signature header against the raw request body.

    Returns normally when the signature is valid and otherwise raises a
    :class:`WebhookSignatureError` subclass describing why it was rejected.

    :param signature_header: value of the signature header sent with the webhook
    :param request_body: raw (unparsed) request body
    :param signing_key: signing key for the webhook endpoint
    """
    timestamp, signatures = _parse_header(signature_header)

    version = _newest_supported_version(signatures)
    if version is None:
        present = ", ".join(f"v{v}" for v in sorted(signatures))
        raise WebhookSignatureUnsupportedVersionError(
            f"Unsupported webhook signature version: header carries only {present}"
        )

    skew = abs(int(time.time()) - int(timestamp))
    if skew > MAX_WEBHOOK_TIMESTAMP_SKEW_SECONDS:
        raise WebhookSignatureTimestampSkewError(
            f"Webhook signature timestamp outside tolerance: off by {skew}s, "
            f"tolerance is {MAX_WEBHOOK_TIMESTAMP_SKEW_SECONDS}s"
        )

    computed = _signature_for_version(version, request_body, signing_key, timestamp)
    if not any(hmac.compare_digest(computed, signature) for signature in signatures[version]):
        raise WebhookSignatureMismatchError("Webhook signature mismatch")


def is_valid_webhook_signature(
    signature_header: str | None, request_body: str | bytes, signing_key: str
) -> bool:
    """Verify a webhook signature header, returning ``False`` instead of raising.

    See :func:`verify_webhook_signature`.
    """
    try:
        verify_webhook_signature(signature_header, request_body, signing_key)
    except WebhookSignatureError:
        return False
    return True


def generate_webhook_signature(payload: str | bytes, signing_key: str, timestamp: str | int) -> str:
    """Compute the hex-encoded HMAC-SHA256 signature for a webhook payload (v1 scheme).

    :param payload: raw (unparsed) request body
    :param signing_key: signing key for the webhook endpoint
    :param timestamp: unix timestamp in seconds, as sent in the signature header
    """
    message = f"{timestamp}.".encode() + _to_bytes(payload)
    return hmac.new(signing_key.encode(), message, hashlib.sha256).hexdigest()


def _to_bytes(value: str | bytes) -> bytes:
    return value.encode() if isinstance(value, str) else value


def _signature_for_version(
    version: int, payload: str | bytes, signing_key: str, timestamp: str
) -> str:
    """Compute the signature for one signing scheme.

    This is the single place a new scheme needs to be added.
    """
    if version == 1:
        return generate_webhook_signature(payload, signing_key, timestamp)
    raise WebhookSignatureUnsupportedVersionError(
        f"Unsupported webhook signature version: v{version}"
    )


def _parse_header(signature_header: str | None) -> tuple[str, dict[int, list[str]]]:
    """Split the header into its timestamp and its signatures keyed by version.

    Elements that are not recognized are ignored, so that a sender adding new
    elements does not break verification here.
    """
    timestamp: str | None = None
    signatures: dict[int, list[str]] = {}

    for element in (signature_header or "").split(","):
        key, separator, value = element.strip().partition("=")
        if not separator:
            continue

        if key == "t":
            if not _TIMESTAMP_VALUE_REGEX.match(value):
                raise WebhookSignatureMalformedHeaderError("Malformed webhook signature header")
            timestamp = value
            continue

        match = _SIGNATURE_KEY_REGEX.match(key)
        if not match:
            continue
        version = int(match.group(1))

        # Only versions this SDK verifies have a signature format it can insist
        # on; anything else is recorded but left unchecked.
        if version in SUPPORTED_WEBHOOK_SIGNATURE_VERSIONS and not _HEX_SIGNATURE_REGEX.match(
            value
        ):
            raise WebhookSignatureMalformedHeaderError("Malformed webhook signature header")

        signatures.setdefault(version, []).append(value)

    if timestamp is None or not signatures:
        raise WebhookSignatureMalformedHeaderError("Malformed webhook signature header")

    return timestamp, signatures


def _newest_supported_version(signatures: dict[int, list[str]]) -> int | None:
    """Pick the highest version present that this SDK can verify.

    Once a sender emits a newer scheme, the older one stops being honored here.
    """
    supported = [v for v in signatures if v in SUPPORTED_WEBHOOK_SIGNATURE_VERSIONS]
    return max(supported) if supported else None
