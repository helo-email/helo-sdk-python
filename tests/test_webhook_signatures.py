from __future__ import annotations

import hashlib
import hmac
import time

import pytest

import sdk_helo_email as helo

SIGNING_KEY = "whsec_test"
BODY = '{"event":"message.delivered"}'


def now() -> str:
    return str(int(time.time()))


def valid_header(timestamp: str | None = None) -> str:
    timestamp = timestamp or now()
    signature = helo.generate_webhook_signature(BODY, SIGNING_KEY, timestamp)
    return f"t={timestamp},v1={signature}"


def test_accepts_a_valid_signature() -> None:
    header = valid_header()

    helo.verify_webhook_signature(header, BODY, SIGNING_KEY)

    assert helo.is_valid_webhook_signature(header, BODY, SIGNING_KEY)
    assert helo.is_valid_webhook_signature(header, BODY.encode(), SIGNING_KEY)


# A sender rolling out a new signing scheme emits every version at once. This SDK
# must keep verifying the versions it knows and ignore the rest, otherwise the
# rollout breaks every receiver that has not upgraded yet.
@pytest.mark.parametrize(
    "header_format",
    [
        "t={t},v1={sig},v2=8badf00d",
        "t={t},v2=8badf00d,v1={sig}",
        "t={t},v1={sig},alg=sha512",
        "t={t}, v1={sig}",
        "v1={sig},t={t}",
        "t={t},v1=8badf00d,v1={sig}",
    ],
)
def test_ignores_unknown_versions_and_elements(header_format: str) -> None:
    timestamp = now()
    signature = helo.generate_webhook_signature(BODY, SIGNING_KEY, timestamp)
    header = header_format.format(t=timestamp, sig=signature)

    assert helo.is_valid_webhook_signature(header, BODY, SIGNING_KEY), header


def test_rejects_a_signature_from_a_different_key() -> None:
    header = valid_header()

    with pytest.raises(helo.WebhookSignatureMismatchError):
        helo.verify_webhook_signature(header, BODY, "wrong-key")
    assert not helo.is_valid_webhook_signature(header, BODY, "wrong-key")


def test_rejects_a_tampered_body() -> None:
    with pytest.raises(helo.WebhookSignatureMismatchError):
        helo.verify_webhook_signature(valid_header(), '{"event":"message.bounced"}', SIGNING_KEY)


def test_rejects_a_stale_timestamp() -> None:
    header = valid_header(str(int(time.time()) - 600))

    with pytest.raises(helo.WebhookSignatureTimestampSkewError, match="tolerance"):
        helo.verify_webhook_signature(header, BODY, SIGNING_KEY)


def test_rejects_a_header_carrying_only_unknown_versions() -> None:
    timestamp = now()
    signature = helo.generate_webhook_signature(BODY, SIGNING_KEY, timestamp)

    with pytest.raises(helo.WebhookSignatureUnsupportedVersionError, match="v2"):
        helo.verify_webhook_signature(f"t={timestamp},v2={signature}", BODY, SIGNING_KEY)


@pytest.mark.parametrize(
    "header_format",
    [
        "garbage",
        "",
        None,
        "t={t},v1=ABCDEF",
        "t={t}",
        "v1={sig}",
        "t=yesterday,v1={sig}",
    ],
)
def test_rejects_malformed_headers(header_format: str | None) -> None:
    timestamp = now()
    signature = helo.generate_webhook_signature(BODY, SIGNING_KEY, timestamp)
    header = None if header_format is None else header_format.format(t=timestamp, sig=signature)

    with pytest.raises(helo.WebhookSignatureMalformedHeaderError):
        helo.verify_webhook_signature(header, BODY, SIGNING_KEY)


def test_treats_a_short_hex_signature_as_a_mismatch_not_malformed() -> None:
    with pytest.raises(helo.WebhookSignatureMismatchError):
        helo.verify_webhook_signature(f"t={now()},v1=abc", BODY, SIGNING_KEY)


def test_every_rejection_shares_one_base_class() -> None:
    assert not helo.is_valid_webhook_signature("garbage", BODY, SIGNING_KEY)

    with pytest.raises(helo.WebhookSignatureError):
        helo.verify_webhook_signature("garbage", BODY, SIGNING_KEY)

    assert issubclass(helo.WebhookSignatureError, helo.HeloError)


def test_generate_matches_the_documented_scheme() -> None:
    expected = hmac.new(
        SIGNING_KEY.encode(), f"1700000000.{BODY}".encode(), hashlib.sha256
    ).hexdigest()

    assert helo.generate_webhook_signature(BODY, SIGNING_KEY, "1700000000") == expected
    assert helo.generate_webhook_signature(BODY.encode(), SIGNING_KEY, 1700000000) == expected
