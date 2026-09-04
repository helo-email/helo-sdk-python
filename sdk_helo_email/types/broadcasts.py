from __future__ import annotations

from datetime import datetime

from pydantic import Field

from .shared import AttachmentDisposition, BroadcastStatus, HeloModel, MailAddress


class BroadcastResponse(HeloModel):
    id: str
    created_at: datetime
    status: BroadcastStatus
    subject: str
    completion: str
    messages: int


class BroadcastContentTemplate(HeloModel):
    subject: str
    html: str | None = None
    text: str | None = None


class BroadcastContentAttachment(HeloModel):
    file_name: str
    disposition: AttachmentDisposition
    size: int


class BroadcastContent(HeloModel):
    from_: MailAddress | None = Field(default=None, alias="from")
    reply_to: list[MailAddress] | None = None
    template: BroadcastContentTemplate | None = None
    attachments: list[BroadcastContentAttachment] | None = None
    tags: list[str] | None = None
    headers: dict[str, str] | None = None
    metadata: dict[str, str] | None = None


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


class RecipientHeaders(HeloModel):
    to: list[MailAddress]
    cc: list[MailAddress] | None = None
    bcc: list[MailAddress] | None = None


class BroadcastFailureResponse(HeloModel):
    recipients: RecipientHeaders
    message_index: int
    error_code: str
    error_message: str


class PaginatedResponseOfBroadcast(HeloModel):
    total_count: int
    results: list[BroadcastResponse]


class PaginatedResponseOfBroadcastFailure(HeloModel):
    total_count: int
    results: list[BroadcastFailureResponse]


class PaginatedResponseOfBroadcastSuppression(HeloModel):
    total_count: int
    results: list[str]
