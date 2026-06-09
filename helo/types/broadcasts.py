from __future__ import annotations

from datetime import datetime
from typing import Any

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
    html: str | None = None
    text: str | None = None


class BroadcastAttachment(HeloModel):
    file_name: str
    disposition: str
    size: int


class BroadcastContent(HeloModel):
    from_: MailAddress | None = None
    reply_to: list[MailAddress] | None = None
    template: BroadcastTemplateContent | None = None
    attachments: list[BroadcastAttachment] | None = None
    tags: list[str] | None = None
    headers: dict[str, Any] | None = None
    metadata: dict[str, Any] | None = None

    @classmethod
    def model_validate(cls, obj: Any, **kwargs: Any) -> BroadcastContent:
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
    results: list[BroadcastResponse]


class RecipientHeaders(HeloModel):
    to: list[MailAddress]
    cc: list[MailAddress] | None = None
    bcc: list[MailAddress] | None = None


class BroadcastFailureResponse(HeloModel):
    recipients: RecipientHeaders
    message_index: int
    error_code: str
    error_message: str


class PaginatedResponseOfBroadcastFailure(HeloModel):
    total_count: int
    results: list[BroadcastFailureResponse]


class PaginatedResponseOfBroadcastSuppression(HeloModel):
    total_count: int
    results: list[str]
