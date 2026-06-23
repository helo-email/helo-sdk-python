from __future__ import annotations

from datetime import datetime
from typing import Any

from .shared import EventType, HeloModel, MailAddress, MailType


class ActivityEvent(HeloModel):
    message_id: str
    channel_id: str
    mail_type: MailType
    mail_source: str | None = None
    event_type: EventType
    timestamp: datetime
    subject: str
    recipients: list[str]
    tags: list[str] | None = None
    metadata: dict[str, Any] | None = None
    details: dict[str, Any] | None = None


class PaginatedEventsResponse(HeloModel):
    after: int | None = None
    total_count: float
    results: list[ActivityEvent]


class Message(HeloModel):
    message_id: str
    channel_id: str
    timestamp: datetime
    mail_type: MailType
    mail_source: str
    delivery_type: str
    status: str
    subject: str
    recipients: list[str]


class PaginatedMessagesResponse(HeloModel):
    after: int | None = None
    total_count: float
    results: list[Message]


class MessageEvent(HeloModel):
    event_type: EventType
    timestamp: datetime
    recipient: str | None = None
    details: dict[str, Any] | None = None


class MessageTracking(HeloModel):
    links: bool
    opens: bool


class MessageDetailsResponse(HeloModel):
    message_id: str
    channel_id: str
    timestamp: datetime
    mail_type: MailType
    mail_source: str
    delivery_type: str
    status: str
    subject: str
    from_: MailAddress
    to: list[MailAddress]
    cc: list[MailAddress] | None = None
    bcc: list[MailAddress] | None = None
    reply_to: list[MailAddress] | None = None
    text: str | None = None
    html: str | None = None
    body: str | None = None
    tags: list[str] | None = None
    headers: dict[str, Any] | None = None
    metadata: dict[str, Any] | None = None
    attachments: list[str] | None = None
    tracking: MessageTracking
    events: list[MessageEvent]

    @classmethod
    def model_validate(cls, obj: Any, **kwargs: Any) -> MessageDetailsResponse:
        if isinstance(obj, dict) and "from" in obj and "from_" not in obj:
            obj = dict(obj)
            obj["from_"] = obj.pop("from")
        return super().model_validate(obj, **kwargs)
