from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class HeloModel(BaseModel):
    """Base for every response model: parses the API's camelCase wire names."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class AttachmentDisposition(str, Enum):
    """How the attachment is presented. Use `attachment` for downloadable files and `inline` for
    embedded content (e.g. images referenced in HTML).
    """

    ATTACHMENT = "attachment"
    INLINE = "inline"


class BroadcastStatus(str, Enum):
    """Current processing state of a broadcast. `accepted` — queued, waiting for the channel to
    become available. `processing` — actively sending messages. `completed` — all messages
    have been processed. `canceled` — stopped before completing.
    """

    ACCEPTED = "accepted"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELED = "canceled"


class DeliveryType(str, Enum):
    """Delivery mode for a channel. `live` sends real emails, whereas `sandbox` accepts and
    processes messages without delivering them to recipients.
    """

    LIVE = "live"
    SANDBOX = "sandbox"


class DnsRecordStatus(str, Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    FAILING = "failing"
    FAILED = "failed"


class DnsRecordType(str, Enum):
    TXT = "txt"
    CNAME = "cname"


class EventType(str, Enum):
    ACCEPTED = "accepted"
    PROCESSED = "processed"
    DELIVERED = "delivered"
    BOUNCED = "bounced"
    OPENED = "opened"
    CLICKED = "clicked"
    COMPLAINED = "complained"
    UNSUBSCRIBED = "unsubscribed"
    RESUBSCRIBED = "resubscribed"


class MailSource(str, Enum):
    API = "api"
    SMTP = "smtp"


class MailType(str, Enum):
    TRANSACTIONAL = "transactional"
    BROADCAST = "broadcast"


class MessageStatus(str, Enum):
    QUEUED = "queued"
    SENT = "sent"


class SuppressionReason(str, Enum):
    BOUNCE = "bounce"
    COMPLAINT = "complaint"
    UNSUBSCRIBE = "unsubscribe"
    MANUAL = "manual"


class WebhookEvent(str, Enum):
    """Email lifecycle event type that can trigger a webhook delivery."""

    ACCEPTED = "accepted"
    PROCESSED = "processed"
    DELIVERED = "delivered"
    BOUNCED = "bounced"
    OPENED = "opened"
    CLICKED = "clicked"
    COMPLAINED = "complained"
    UNSUBSCRIBED = "unsubscribed"
    RESUBSCRIBED = "resubscribed"
    DOMAIN_KEY_VERIFIED = "domain-key-verified"
    DOMAIN_KEY_VERIFICATION_FAILED = "domain-key-verification-failed"
    RETURN_PATH_DOMAIN_VERIFIED = "return-path-domain-verified"
    RETURN_PATH_DOMAIN_VERIFICATION_FAILED = "return-path-domain-verification-failed"


class MailAddress(HeloModel):
    email: str
    name: str | None = None
