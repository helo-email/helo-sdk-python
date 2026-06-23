from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from .._utils import build_body
from ..types.params import (
    AttachmentParam,
    HeadersParam,
    MailAddressParam,
    MetadataParam,
    TemplateParam,
    TrackingParam,
)
from ..types.sending import (
    SendBroadcastResponse,
    SendMessageAcceptedResponse,
    SendMessageBatchResponse,
)
from ._base import AsyncBaseResource, BaseResource


def _sending_headers(
    channel_id: str | None,
    idempotency_key: str | None,
) -> dict[str, str] | None:
    headers: dict[str, str] = {}
    if channel_id is not None:
        headers["X-Helo-Channel-Id"] = channel_id
    if idempotency_key is not None:
        headers["X-Helo-Idempotency-Key"] = idempotency_key
    return headers or None


def _message_body(
    *,
    from_: MailAddressParam,
    to: Sequence[MailAddressParam],
    cc: Sequence[MailAddressParam] | None,
    bcc: Sequence[MailAddressParam] | None,
    reply_to: Sequence[MailAddressParam] | None,
    subject: str | None,
    html: str | None,
    text: str | None,
    template: TemplateParam | None,
    tracking: TrackingParam | None,
    attachments: Sequence[AttachmentParam] | None,
    tags: Sequence[str] | None,
    headers: HeadersParam | None,
    metadata: MetadataParam | None,
) -> dict[str, Any]:
    return build_body(
        from_=from_,
        to=to,
        cc=cc,
        bcc=bcc,
        reply_to=reply_to,
        subject=subject,
        html=html,
        text=text,
        template=template,
        tracking=tracking,
        attachments=attachments,
        tags=tags,
        headers=headers,
        metadata=metadata,
    )


def _broadcast_body(
    *,
    from_: MailAddressParam,
    messages: Sequence[dict[str, Any]],
    template: TemplateParam,
    reply_to: Sequence[MailAddressParam] | None,
    tracking: TrackingParam | None,
    attachments: Sequence[AttachmentParam] | None,
    tags: Sequence[str] | None,
    headers: HeadersParam | None,
    metadata: MetadataParam | None,
) -> dict[str, Any]:
    return build_body(
        from_=from_,
        messages=messages,
        template=template,
        reply_to=reply_to,
        tracking=tracking,
        attachments=attachments,
        tags=tags,
        headers=headers,
        metadata=metadata,
    )


class SendingResource(BaseResource):
    def transactional(
        self,
        *,
        from_: MailAddressParam,
        to: Sequence[MailAddressParam],
        cc: Sequence[MailAddressParam] | None = None,
        bcc: Sequence[MailAddressParam] | None = None,
        reply_to: Sequence[MailAddressParam] | None = None,
        subject: str | None = None,
        html: str | None = None,
        text: str | None = None,
        template: TemplateParam | None = None,
        tracking: TrackingParam | None = None,
        attachments: Sequence[AttachmentParam] | None = None,
        tags: Sequence[str] | None = None,
        headers: HeadersParam | None = None,
        metadata: MetadataParam | None = None,
        channel_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> SendMessageAcceptedResponse:
        body = _message_body(
            from_=from_, to=to, cc=cc, bcc=bcc, reply_to=reply_to, subject=subject,
            html=html, text=text, template=template, tracking=tracking,
            attachments=attachments, tags=tags, headers=headers, metadata=metadata,
        )
        data = self._http.post(
            "/send/transactional",
            json=body,
            headers=_sending_headers(channel_id, idempotency_key),
        )
        return SendMessageAcceptedResponse.model_validate(data)

    def transactional_batch(
        self,
        *,
        requests: Sequence[dict[str, Any]],
        channel_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> SendMessageBatchResponse:
        data = self._http.post(
            "/send/transactional/batch",
            json={"requests": requests},
            headers=_sending_headers(channel_id, idempotency_key),
        )
        return SendMessageBatchResponse.model_validate(data)

    def broadcast(
        self,
        *,
        from_: MailAddressParam,
        messages: Sequence[dict[str, Any]],
        template: TemplateParam,
        reply_to: Sequence[MailAddressParam] | None = None,
        tracking: TrackingParam | None = None,
        attachments: Sequence[AttachmentParam] | None = None,
        tags: Sequence[str] | None = None,
        headers: HeadersParam | None = None,
        metadata: MetadataParam | None = None,
        channel_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> SendBroadcastResponse:
        body = _broadcast_body(
            from_=from_, messages=messages, template=template, reply_to=reply_to,
            tracking=tracking, attachments=attachments, tags=tags, headers=headers,
            metadata=metadata,
        )
        data = self._http.post(
            "/send/broadcast",
            json=body,
            headers=_sending_headers(channel_id, idempotency_key),
        )
        return SendBroadcastResponse.model_validate(data)

    def broadcast_message(
        self,
        *,
        from_: MailAddressParam,
        to: Sequence[MailAddressParam],
        cc: Sequence[MailAddressParam] | None = None,
        bcc: Sequence[MailAddressParam] | None = None,
        reply_to: Sequence[MailAddressParam] | None = None,
        subject: str | None = None,
        html: str | None = None,
        text: str | None = None,
        template: TemplateParam | None = None,
        tracking: TrackingParam | None = None,
        attachments: Sequence[AttachmentParam] | None = None,
        tags: Sequence[str] | None = None,
        headers: HeadersParam | None = None,
        metadata: MetadataParam | None = None,
        channel_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> SendMessageAcceptedResponse:
        body = _message_body(
            from_=from_, to=to, cc=cc, bcc=bcc, reply_to=reply_to, subject=subject,
            html=html, text=text, template=template, tracking=tracking,
            attachments=attachments, tags=tags, headers=headers, metadata=metadata,
        )
        data = self._http.post(
            "/send/broadcast/message",
            json=body,
            headers=_sending_headers(channel_id, idempotency_key),
        )
        return SendMessageAcceptedResponse.model_validate(data)


class AsyncSendingResource(AsyncBaseResource):
    async def transactional(
        self,
        *,
        from_: MailAddressParam,
        to: Sequence[MailAddressParam],
        cc: Sequence[MailAddressParam] | None = None,
        bcc: Sequence[MailAddressParam] | None = None,
        reply_to: Sequence[MailAddressParam] | None = None,
        subject: str | None = None,
        html: str | None = None,
        text: str | None = None,
        template: TemplateParam | None = None,
        tracking: TrackingParam | None = None,
        attachments: Sequence[AttachmentParam] | None = None,
        tags: Sequence[str] | None = None,
        headers: HeadersParam | None = None,
        metadata: MetadataParam | None = None,
        channel_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> SendMessageAcceptedResponse:
        body = _message_body(
            from_=from_, to=to, cc=cc, bcc=bcc, reply_to=reply_to, subject=subject,
            html=html, text=text, template=template, tracking=tracking,
            attachments=attachments, tags=tags, headers=headers, metadata=metadata,
        )
        data = await self._http.post(
            "/send/transactional",
            json=body,
            headers=_sending_headers(channel_id, idempotency_key),
        )
        return SendMessageAcceptedResponse.model_validate(data)

    async def transactional_batch(
        self,
        *,
        requests: Sequence[dict[str, Any]],
        channel_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> SendMessageBatchResponse:
        data = await self._http.post(
            "/send/transactional/batch",
            json={"requests": requests},
            headers=_sending_headers(channel_id, idempotency_key),
        )
        return SendMessageBatchResponse.model_validate(data)

    async def broadcast(
        self,
        *,
        from_: MailAddressParam,
        messages: Sequence[dict[str, Any]],
        template: TemplateParam,
        reply_to: Sequence[MailAddressParam] | None = None,
        tracking: TrackingParam | None = None,
        attachments: Sequence[AttachmentParam] | None = None,
        tags: Sequence[str] | None = None,
        headers: HeadersParam | None = None,
        metadata: MetadataParam | None = None,
        channel_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> SendBroadcastResponse:
        body = _broadcast_body(
            from_=from_, messages=messages, template=template, reply_to=reply_to,
            tracking=tracking, attachments=attachments, tags=tags, headers=headers,
            metadata=metadata,
        )
        data = await self._http.post(
            "/send/broadcast",
            json=body,
            headers=_sending_headers(channel_id, idempotency_key),
        )
        return SendBroadcastResponse.model_validate(data)

    async def broadcast_message(
        self,
        *,
        from_: MailAddressParam,
        to: Sequence[MailAddressParam],
        cc: Sequence[MailAddressParam] | None = None,
        bcc: Sequence[MailAddressParam] | None = None,
        reply_to: Sequence[MailAddressParam] | None = None,
        subject: str | None = None,
        html: str | None = None,
        text: str | None = None,
        template: TemplateParam | None = None,
        tracking: TrackingParam | None = None,
        attachments: Sequence[AttachmentParam] | None = None,
        tags: Sequence[str] | None = None,
        headers: HeadersParam | None = None,
        metadata: MetadataParam | None = None,
        channel_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> SendMessageAcceptedResponse:
        body = _message_body(
            from_=from_, to=to, cc=cc, bcc=bcc, reply_to=reply_to, subject=subject,
            html=html, text=text, template=template, tracking=tracking,
            attachments=attachments, tags=tags, headers=headers, metadata=metadata,
        )
        data = await self._http.post(
            "/send/broadcast/message",
            json=body,
            headers=_sending_headers(channel_id, idempotency_key),
        )
        return SendMessageAcceptedResponse.model_validate(data)
