from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from .shared import EventType, HeloModel, MailAddress, MailType


class ActivityEvent(HeloModel):
    message_id: str
    channel_id: str
    mail_type: MailType
    mail_source: Optional[str] = None
    event_type: EventType
    timestamp: datetime
    subject: str
    recipients: List[str]
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    details: Optional[Dict[str, Any]] = None


class PaginatedEventsResponse(HeloModel):
    after: Optional[int] = None
    total_count: float
    results: List[ActivityEvent]


class Message(HeloModel):
    message_id: str
    channel_id: str
    timestamp: datetime
    mail_type: MailType
    mail_source: str
    delivery_type: str
    status: str
    subject: str
    recipients: List[str]


class PaginatedMessagesResponse(HeloModel):
    after: Optional[int] = None
    total_count: float
    results: List[Message]


class MessageEvent(HeloModel):
    event_type: EventType
    timestamp: datetime
    recipient: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


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
    to: List[MailAddress]
    cc: Optional[List[MailAddress]] = None
    bcc: Optional[List[MailAddress]] = None
    reply_to: Optional[List[MailAddress]] = None
    text: Optional[str] = None
    html: Optional[str] = None
    body: Optional[str] = None
    tags: Optional[List[str]] = None
    headers: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    attachments: Optional[List[str]] = None
    tracking: MessageTracking
    events: List[MessageEvent]

    @classmethod
    def model_validate(cls, obj: Any, **kwargs: Any) -> "MessageDetailsResponse":
        if isinstance(obj, dict) and "from" in obj and "from_" not in obj:
            obj = dict(obj)
            obj["from_"] = obj.pop("from")
        return super().model_validate(obj, **kwargs)
