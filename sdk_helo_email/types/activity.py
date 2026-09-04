from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from .shared import (
    AttachmentDisposition,
    DeliveryType,
    EventType,
    HeloModel,
    MailSource,
    MailType,
    MessageStatus,
)


class ActivityMailAddress(HeloModel):
    email: str
    name: str | None = None


class ActivityEvent(HeloModel):
    message_id: str
    channel_id: str
    mail_type: MailType
    mail_source: MailSource | None = None
    event_type: EventType
    timestamp: datetime
    subject: str
    recipients: list[str]
    tags: list[str] | None = None
    metadata: dict[str, str] | None = None
    details: dict[str, Any] | None = None


class PaginatedEventsResponse(HeloModel):
    after: int | None = None
    total_count: float
    results: list[ActivityEvent]


class MessageStatistics(HeloModel):
    delivered: int
    bounced: int
    opened: int
    clicked: int
    complained: int
    unsubscribed: int


class Message(HeloModel):
    message_id: str
    channel_id: str
    timestamp: datetime
    mail_type: MailType
    mail_source: MailSource
    delivery_type: DeliveryType
    status: MessageStatus
    subject: str
    recipients: list[str]
    tags: list[str] | None = None
    statistics: MessageStatistics


class PaginatedMessagesResponse(HeloModel):
    after: int | None = None
    total_count: float
    results: list[Message]


class MessageDetailsResponseAttachment(HeloModel):
    file_name: str
    disposition: AttachmentDisposition
    size: float


class MessageDetailsResponseTracking(HeloModel):
    links: bool
    opens: bool


class MessageDetailsResponseEvent(HeloModel):
    event_type: EventType
    timestamp: datetime
    recipients: list[str]
    details: dict[str, Any] | None = None


class MessageDetailsResponse(HeloModel):
    message_id: str
    channel_id: str
    timestamp: datetime
    mail_type: MailType
    mail_source: MailSource
    delivery_type: DeliveryType
    status: MessageStatus
    subject: str
    from_: ActivityMailAddress = Field(alias="from")
    to: list[ActivityMailAddress]
    cc: list[ActivityMailAddress] | None = None
    bcc: list[ActivityMailAddress] | None = None
    reply_to: list[ActivityMailAddress] | None = None
    text: str | None = None
    html: str | None = None
    body: str | None = None
    tags: list[str] | None = None
    headers: dict[str, str] | None = None
    metadata: dict[str, str] | None = None
    attachments: list[MessageDetailsResponseAttachment] | None = None
    tracking: MessageDetailsResponseTracking
    events: list[MessageDetailsResponseEvent]
    statistics: MessageStatistics | None = None
