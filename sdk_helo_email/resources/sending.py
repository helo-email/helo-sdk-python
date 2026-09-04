from __future__ import annotations

from collections.abc import Sequence

from .._utils import build_body, build_headers
from ..types.params import (
    AttachmentParam,
    MailAddressParam,
    SendBroadcastRequestMessageParam,
    SendBroadcastRequestTemplateParam,
    SendBroadcastRequestTrackingParam,
    SendMessageRequestParam,
    SendMessageRequestTemplateParam,
    SendMessageRequestTrackingParam,
)
from ..types.sending import (
    SendBroadcastResponse,
    SendMessageAcceptedResponse,
    SendMessageBatchResponse,
)
from ._base import AsyncBaseResource, BaseResource


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
        template: SendMessageRequestTemplateParam | None = None,
        tracking: SendMessageRequestTrackingParam | None = None,
        attachments: Sequence[AttachmentParam] | None = None,
        tags: Sequence[str] | None = None,
        headers: dict[str, str] | None = None,
        metadata: dict[str, str] | None = None,
        channel_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> SendMessageAcceptedResponse:
        """Send a transactional email"""

        body = build_body(
            from_=from_,
            to=[str(item) for item in to] if to else None,
            cc=[str(item) for item in cc] if cc else None,
            bcc=[str(item) for item in bcc] if bcc else None,
            reply_to=[str(item) for item in reply_to] if reply_to else None,
            subject=subject,
            html=html,
            text=text,
            template=template,
            tracking=tracking,
            attachments=[str(item) for item in attachments] if attachments else None,
            tags=tags if tags else None,
            headers=headers,
            metadata=metadata,
        )
        headers = build_headers(
            **{"X-Helo-Channel-Id": channel_id},
            **{"X-Helo-Idempotency-Key": idempotency_key},
        )
        data = self._http.post("/send/transactional", json=body, headers=headers)
        return SendMessageAcceptedResponse.model_validate(data)

    def transactional_batch(
        self,
        *,
        requests: Sequence[SendMessageRequestParam],
        channel_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> SendMessageBatchResponse:
        """Send transactional emails in batch"""

        body = build_body(
            requests=[str(item) for item in requests] if requests else None,
        )
        headers = build_headers(
            **{"X-Helo-Channel-Id": channel_id},
            **{"X-Helo-Idempotency-Key": idempotency_key},
        )
        data = self._http.post("/send/transactional/batch", json=body, headers=headers)
        return SendMessageBatchResponse.model_validate(data)

    def broadcast(
        self,
        *,
        from_: MailAddressParam,
        template: SendBroadcastRequestTemplateParam,
        messages: Sequence[SendBroadcastRequestMessageParam],
        reply_to: Sequence[MailAddressParam] | None = None,
        tracking: SendBroadcastRequestTrackingParam | None = None,
        attachments: Sequence[AttachmentParam] | None = None,
        tags: Sequence[str] | None = None,
        headers: dict[str, str] | None = None,
        metadata: dict[str, str] | None = None,
        channel_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> SendBroadcastResponse:
        """Send a broadcast email"""

        body = build_body(
            from_=from_,
            template=template,
            messages=[str(item) for item in messages] if messages else None,
            reply_to=[str(item) for item in reply_to] if reply_to else None,
            tracking=tracking,
            attachments=[str(item) for item in attachments] if attachments else None,
            tags=tags if tags else None,
            headers=headers,
            metadata=metadata,
        )
        headers = build_headers(
            **{"X-Helo-Channel-Id": channel_id},
            **{"X-Helo-Idempotency-Key": idempotency_key},
        )
        data = self._http.post("/send/broadcast", json=body, headers=headers)
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
        template: SendMessageRequestTemplateParam | None = None,
        tracking: SendMessageRequestTrackingParam | None = None,
        attachments: Sequence[AttachmentParam] | None = None,
        tags: Sequence[str] | None = None,
        headers: dict[str, str] | None = None,
        metadata: dict[str, str] | None = None,
        channel_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> SendMessageAcceptedResponse:
        """Send a single broadcast email"""

        body = build_body(
            from_=from_,
            to=[str(item) for item in to] if to else None,
            cc=[str(item) for item in cc] if cc else None,
            bcc=[str(item) for item in bcc] if bcc else None,
            reply_to=[str(item) for item in reply_to] if reply_to else None,
            subject=subject,
            html=html,
            text=text,
            template=template,
            tracking=tracking,
            attachments=[str(item) for item in attachments] if attachments else None,
            tags=tags if tags else None,
            headers=headers,
            metadata=metadata,
        )
        headers = build_headers(
            **{"X-Helo-Channel-Id": channel_id},
            **{"X-Helo-Idempotency-Key": idempotency_key},
        )
        data = self._http.post("/send/broadcast/message", json=body, headers=headers)
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
        template: SendMessageRequestTemplateParam | None = None,
        tracking: SendMessageRequestTrackingParam | None = None,
        attachments: Sequence[AttachmentParam] | None = None,
        tags: Sequence[str] | None = None,
        headers: dict[str, str] | None = None,
        metadata: dict[str, str] | None = None,
        channel_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> SendMessageAcceptedResponse:
        """Send a transactional email"""

        body = build_body(
            from_=from_,
            to=[str(item) for item in to] if to else None,
            cc=[str(item) for item in cc] if cc else None,
            bcc=[str(item) for item in bcc] if bcc else None,
            reply_to=[str(item) for item in reply_to] if reply_to else None,
            subject=subject,
            html=html,
            text=text,
            template=template,
            tracking=tracking,
            attachments=[str(item) for item in attachments] if attachments else None,
            tags=tags if tags else None,
            headers=headers,
            metadata=metadata,
        )
        headers = build_headers(
            **{"X-Helo-Channel-Id": channel_id},
            **{"X-Helo-Idempotency-Key": idempotency_key},
        )
        data = await self._http.post("/send/transactional", json=body, headers=headers)
        return SendMessageAcceptedResponse.model_validate(data)

    async def transactional_batch(
        self,
        *,
        requests: Sequence[SendMessageRequestParam],
        channel_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> SendMessageBatchResponse:
        """Send transactional emails in batch"""

        body = build_body(
            requests=[str(item) for item in requests] if requests else None,
        )
        headers = build_headers(
            **{"X-Helo-Channel-Id": channel_id},
            **{"X-Helo-Idempotency-Key": idempotency_key},
        )
        data = await self._http.post("/send/transactional/batch", json=body, headers=headers)
        return SendMessageBatchResponse.model_validate(data)

    async def broadcast(
        self,
        *,
        from_: MailAddressParam,
        template: SendBroadcastRequestTemplateParam,
        messages: Sequence[SendBroadcastRequestMessageParam],
        reply_to: Sequence[MailAddressParam] | None = None,
        tracking: SendBroadcastRequestTrackingParam | None = None,
        attachments: Sequence[AttachmentParam] | None = None,
        tags: Sequence[str] | None = None,
        headers: dict[str, str] | None = None,
        metadata: dict[str, str] | None = None,
        channel_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> SendBroadcastResponse:
        """Send a broadcast email"""

        body = build_body(
            from_=from_,
            template=template,
            messages=[str(item) for item in messages] if messages else None,
            reply_to=[str(item) for item in reply_to] if reply_to else None,
            tracking=tracking,
            attachments=[str(item) for item in attachments] if attachments else None,
            tags=tags if tags else None,
            headers=headers,
            metadata=metadata,
        )
        headers = build_headers(
            **{"X-Helo-Channel-Id": channel_id},
            **{"X-Helo-Idempotency-Key": idempotency_key},
        )
        data = await self._http.post("/send/broadcast", json=body, headers=headers)
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
        template: SendMessageRequestTemplateParam | None = None,
        tracking: SendMessageRequestTrackingParam | None = None,
        attachments: Sequence[AttachmentParam] | None = None,
        tags: Sequence[str] | None = None,
        headers: dict[str, str] | None = None,
        metadata: dict[str, str] | None = None,
        channel_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> SendMessageAcceptedResponse:
        """Send a single broadcast email"""

        body = build_body(
            from_=from_,
            to=[str(item) for item in to] if to else None,
            cc=[str(item) for item in cc] if cc else None,
            bcc=[str(item) for item in bcc] if bcc else None,
            reply_to=[str(item) for item in reply_to] if reply_to else None,
            subject=subject,
            html=html,
            text=text,
            template=template,
            tracking=tracking,
            attachments=[str(item) for item in attachments] if attachments else None,
            tags=tags if tags else None,
            headers=headers,
            metadata=metadata,
        )
        headers = build_headers(
            **{"X-Helo-Channel-Id": channel_id},
            **{"X-Helo-Idempotency-Key": idempotency_key},
        )
        data = await self._http.post("/send/broadcast/message", json=body, headers=headers)
        return SendMessageAcceptedResponse.model_validate(data)
