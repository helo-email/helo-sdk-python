from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class HeloModel(BaseModel):
    """Base for every response model: parses the API's camelCase wire names."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class HeloEnum(str, Enum):
    """Base for every enum. A value this version of the SDK doesn't know, one the API
    added later, becomes a new member instead of failing to parse."""

    @classmethod
    def _missing_(cls, value: object) -> Any:
        if not isinstance(value, str):
            return None
        member = str.__new__(cls, value)
        member._name_ = value.upper()
        member._value_ = value
        return member


class AttachmentDisposition(HeloEnum):
    """How the attachment is presented. Use `attachment` for downloadable files and `inline` for
    embedded content (e.g. images referenced in HTML).
    """

    ATTACHMENT = "attachment"
    INLINE = "inline"


class BroadcastStatus(HeloEnum):
    """Current processing state of a broadcast. `accepted` — queued, waiting for the channel to
    become available. `processing` — actively sending messages. `completed` — all messages
    have been processed. `canceled` — stopped before completing.
    """

    ACCEPTED = "accepted"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELED = "canceled"


class DeliveryType(HeloEnum):
    """Delivery mode for a channel. `live` sends real emails, whereas `sandbox` accepts and
    processes messages without delivering them to recipients.
    """

    LIVE = "live"
    SANDBOX = "sandbox"


class DnsRecordStatus(HeloEnum):
    PENDING = "pending"
    VERIFIED = "verified"
    FAILING = "failing"
    FAILED = "failed"


class DnsRecordType(HeloEnum):
    TXT = "txt"
    CNAME = "cname"


class EventType(HeloEnum):
    ACCEPTED = "accepted"
    PROCESSED = "processed"
    DELIVERED = "delivered"
    BOUNCED = "bounced"
    OPENED = "opened"
    CLICKED = "clicked"
    COMPLAINED = "complained"
    UNSUBSCRIBED = "unsubscribed"
    RESUBSCRIBED = "resubscribed"


class MailSource(HeloEnum):
    API = "api"
    SMTP = "smtp"


class MailType(HeloEnum):
    TRANSACTIONAL = "transactional"
    BROADCAST = "broadcast"


class MessageStatus(HeloEnum):
    QUEUED = "queued"
    SENT = "sent"


class SuppressionReason(HeloEnum):
    BOUNCE = "bounce"
    COMPLAINT = "complaint"
    UNSUBSCRIBE = "unsubscribe"
    MANUAL = "manual"


class WebhookEvent(HeloEnum):
    """Email lifecycle event type that can trigger a webhook delivery."""

    MESSAGE_ACCEPTED = "message-accepted"
    MESSAGE_PROCESSED = "message-processed"
    EMAIL_DELIVERED = "email-delivered"
    EMAIL_BOUNCED = "email-bounced"
    EMAIL_OPENED = "email-opened"
    LINK_CLICKED = "link-clicked"
    RECIPIENT_COMPLAINED = "recipient-complained"
    RECIPIENT_UNSUBSCRIBED = "recipient-unsubscribed"
    RECIPIENT_RESUBSCRIBED = "recipient-resubscribed"
    DOMAIN_KEY_VERIFIED = "domain-key-verified"
    DOMAIN_KEY_VERIFICATION_FAILED = "domain-key-verification-failed"
    RETURN_PATH_DOMAIN_VERIFIED = "return-path-domain-verified"
    RETURN_PATH_DOMAIN_VERIFICATION_FAILED = "return-path-domain-verification-failed"


class MailAddress(HeloModel):
    email: str
    name: str | None = None
