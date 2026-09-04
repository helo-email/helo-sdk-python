from __future__ import annotations

from typing import Any

from pydantic import Field

from .shared import AttachmentDisposition, HeloModel, MailAddress


class Attachment(HeloModel):
    content: str
    content_id: str | None = None
    content_type: str | None = None
    file_name: str
    disposition: AttachmentDisposition


class SendBroadcastRequestTemplate(HeloModel):
    """Email template applied to every message in the broadcast. At least one of `html` or `text`
    is required.
    """

    subject: str
    html: str | None = None
    text: str | None = None
    inline_styles: bool | None = None
    data: dict[str, Any] | None = None


class SendBroadcastRequestTracking(HeloModel):
    """Override channel-level open and link tracking settings."""

    opens: bool | None = None
    links: bool | None = None


class SendBroadcastRequestMessage(HeloModel):
    to: list[MailAddress]
    cc: list[MailAddress] | None = None
    bcc: list[MailAddress] | None = None
    tags: list[str] | None = None
    headers: dict[str, str] | None = None
    metadata: dict[str, str] | None = None
    data: dict[str, Any] | None = None


class SendBroadcastRequest(HeloModel):
    from_: MailAddress = Field(alias="from")
    reply_to: list[MailAddress] | None = None
    template: SendBroadcastRequestTemplate
    tracking: SendBroadcastRequestTracking | None = None
    attachments: list[Attachment] | None = None
    tags: list[str] | None = None
    headers: dict[str, str] | None = None
    metadata: dict[str, str] | None = None
    messages: list[SendBroadcastRequestMessage]


class SendBroadcastResponse(HeloModel):
    status: str | None = None
    broadcast_id: str | None = None


class SendMessageRequestTemplate(HeloModel):
    subject: str | None = None
    html: str | None = None
    text: str | None = None
    inline_styles: bool | None = None
    data: dict[str, Any] | None = None


class SendMessageRequestTracking(HeloModel):
    opens: bool | None = None
    links: bool | None = None


class SendMessageRequest(HeloModel):
    from_: MailAddress = Field(alias="from")
    to: list[MailAddress]
    cc: list[MailAddress] | None = None
    bcc: list[MailAddress] | None = None
    reply_to: list[MailAddress] | None = None
    subject: str | None = None
    html: str | None = None
    text: str | None = None
    template: SendMessageRequestTemplate | None = None
    tracking: SendMessageRequestTracking | None = None
    attachments: list[Attachment] | None = None
    tags: list[str] | None = None
    headers: dict[str, str] | None = None
    metadata: dict[str, str] | None = None


class SendMessageResponse(HeloModel):
    status: str
    message_id: str | None = None
    suppressions: list[str] | None = None
    error_code: str | None = None
    error_message: str | None = None


class SendMessageAcceptedResponse(HeloModel):
    status: str | None = None
    message_id: str | None = None
    suppressions: list[str] | None = None


class SendMessageFailedResponse(HeloModel):
    status: str
    error_code: str
    error_message: str


class SendMessageBatchRequest(HeloModel):
    requests: list[SendMessageRequest]


class SendMessageBatchResponse(HeloModel):
    responses: list[SendMessageResponse]
