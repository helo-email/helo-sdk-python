from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from .shared import BroadcastStatus, HeloModel, MailAddress


class BroadcastTracking(HeloModel):
    opens: bool
    links: bool


class BroadcastStatistics(HeloModel):
    sent: int
    delivered: int
    bounced: int
    opened: int
    clicked: int
    complained: int
    unsubscribed: int


class BroadcastTemplateContent(HeloModel):
    subject: str
    html: Optional[str] = None
    text: Optional[str] = None


class BroadcastAttachment(HeloModel):
    file_name: str
    disposition: str
    size: int


class BroadcastContent(HeloModel):
    from_: Optional[MailAddress] = None
    reply_to: Optional[List[MailAddress]] = None
    template: Optional[BroadcastTemplateContent] = None
    attachments: Optional[List[BroadcastAttachment]] = None
    tags: Optional[List[str]] = None
    headers: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

    @classmethod
    def model_validate(cls, obj: Any, **kwargs: Any) -> "BroadcastContent":
        if isinstance(obj, dict) and "from" in obj and "from_" not in obj:
            obj = dict(obj)
            obj["from_"] = obj.pop("from")
        return super().model_validate(obj, **kwargs)


class BroadcastResponse(HeloModel):
    id: str
    created_at: datetime
    status: BroadcastStatus
    subject: str
    completion: str
    messages: int


class BroadcastDetailsResponse(HeloModel):
    id: str
    created_at: datetime
    status: BroadcastStatus
    subject: str
    completion: str
    messages: int
    failed: int
    suppressed: int
    content: BroadcastContent
    tracking: BroadcastTracking
    statistics: BroadcastStatistics


class PaginatedResponseOfBroadcast(HeloModel):
    total_count: int
    results: List[BroadcastResponse]


class RecipientHeaders(HeloModel):
    to: List[MailAddress]
    cc: Optional[List[MailAddress]] = None
    bcc: Optional[List[MailAddress]] = None


class BroadcastFailureResponse(HeloModel):
    recipients: RecipientHeaders
    message_index: int
    error_code: str
    error_message: str


class PaginatedResponseOfBroadcastFailure(HeloModel):
    total_count: int
    results: List[BroadcastFailureResponse]


class PaginatedResponseOfBroadcastSuppression(HeloModel):
    total_count: int
    results: List[str]
