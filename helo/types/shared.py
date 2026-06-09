from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class HeloModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class DeliveryType(str, Enum):
    LIVE = "live"
    SANDBOX = "sandbox"


class MailType(str, Enum):
    TRANSACTIONAL = "transactional"
    BROADCAST = "broadcast"


class EventType(str, Enum):
    ACCEPTED = "accepted"
    PROCESSED = "processed"
    DELIVERED = "delivered"
    BOUNCED = "bounced"
    OPENED = "opened"
    CLICKED = "clicked"
    COMPLAINED = "complained"
    UNSUBSCRIBED = "unsubscribed"


class AttachmentDisposition(str, Enum):
    ATTACHMENT = "attachment"
    INLINE = "inline"


class DnsRecordStatus(str, Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    FAILING = "failing"
    FAILED = "failed"


class DnsRecordType(str, Enum):
    TXT = "txt"
    CNAME = "cname"


class SuppressionReason(str, Enum):
    BOUNCE = "bounce"
    COMPLAINT = "complaint"
    UNSUBSCRIBE = "unsubscribe"
    MANUAL = "manual"


class BroadcastStatus(str, Enum):
    ACCEPTED = "accepted"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class WebhookEvent(str, Enum):
    ACCEPTED = "accepted"
    PROCESSED = "processed"
    BOUNCED = "bounced"
    DELIVERED = "delivered"
    OPENED = "opened"
    CLICKED = "clicked"
    COMPLAINED = "complained"
    UNSUBSCRIBED = "unsubscribed"
    RESUBSCRIBED = "resubscribed"


class MailAddress(HeloModel):
    email: str
    name: str | None = None
