from __future__ import annotations

from collections.abc import Sequence
from uuid import uuid4

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
    def send_transactional(
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
        headers = build_headers(
            **{"X-Helo-Channel-Id": channel_id},
            # Generated once per call, so a retry is recognized as the same request.
            **{"X-Helo-Idempotency-Key": idempotency_key or str(uuid4())},
        )
        data = self._http.post("/send/transactional", json=body, headers=headers)
        return SendMessageAcceptedResponse.model_validate(data)

    def send_transactional_batch(
        self,
        *,
        requests: Sequence[SendMessageRequestParam],
        channel_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> SendMessageBatchResponse:
        """Send transactional emails in batch"""

        body = build_body(
            requests=requests,
        )
        headers = build_headers(
            **{"X-Helo-Channel-Id": channel_id},
            # Generated once per call, so a retry is recognized as the same request.
            **{"X-Helo-Idempotency-Key": idempotency_key or str(uuid4())},
        )
        data = self._http.post("/send/transactional/batch", json=body, headers=headers)
        return SendMessageBatchResponse.model_validate(data)

    def send_broadcast(
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
        """Send a broadcast"""

        body = build_body(
            from_=from_,
            template=template,
            messages=messages,
            reply_to=reply_to,
            tracking=tracking,
            attachments=attachments,
            tags=tags,
            headers=headers,
            metadata=metadata,
        )
        headers = build_headers(
            **{"X-Helo-Channel-Id": channel_id},
            # Generated once per call, so a retry is recognized as the same request.
            **{"X-Helo-Idempotency-Key": idempotency_key or str(uuid4())},
        )
        data = self._http.post("/send/broadcast", json=body, headers=headers)
        return SendBroadcastResponse.model_validate(data)

    def send_broadcast_message(
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
        headers = build_headers(
            **{"X-Helo-Channel-Id": channel_id},
            # Generated once per call, so a retry is recognized as the same request.
            **{"X-Helo-Idempotency-Key": idempotency_key or str(uuid4())},
        )
        data = self._http.post("/send/broadcast/message", json=body, headers=headers)
        return SendMessageAcceptedResponse.model_validate(data)


class AsyncSendingResource(AsyncBaseResource):
    async def send_transactional(
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
        headers = build_headers(
            **{"X-Helo-Channel-Id": channel_id},
            # Generated once per call, so a retry is recognized as the same request.
            **{"X-Helo-Idempotency-Key": idempotency_key or str(uuid4())},
        )
        data = await self._http.post("/send/transactional", json=body, headers=headers)
        return SendMessageAcceptedResponse.model_validate(data)

    async def send_transactional_batch(
        self,
        *,
        requests: Sequence[SendMessageRequestParam],
        channel_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> SendMessageBatchResponse:
        """Send transactional emails in batch"""

        body = build_body(
            requests=requests,
        )
        headers = build_headers(
            **{"X-Helo-Channel-Id": channel_id},
            # Generated once per call, so a retry is recognized as the same request.
            **{"X-Helo-Idempotency-Key": idempotency_key or str(uuid4())},
        )
        data = await self._http.post("/send/transactional/batch", json=body, headers=headers)
        return SendMessageBatchResponse.model_validate(data)

    async def send_broadcast(
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
        """Send a broadcast"""

        body = build_body(
            from_=from_,
            template=template,
            messages=messages,
            reply_to=reply_to,
            tracking=tracking,
            attachments=attachments,
            tags=tags,
            headers=headers,
            metadata=metadata,
        )
        headers = build_headers(
            **{"X-Helo-Channel-Id": channel_id},
            # Generated once per call, so a retry is recognized as the same request.
            **{"X-Helo-Idempotency-Key": idempotency_key or str(uuid4())},
        )
        data = await self._http.post("/send/broadcast", json=body, headers=headers)
        return SendBroadcastResponse.model_validate(data)

    async def send_broadcast_message(
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
        headers = build_headers(
            **{"X-Helo-Channel-Id": channel_id},
            # Generated once per call, so a retry is recognized as the same request.
            **{"X-Helo-Idempotency-Key": idempotency_key or str(uuid4())},
        )
        data = await self._http.post("/send/broadcast/message", json=body, headers=headers)
        return SendMessageAcceptedResponse.model_validate(data)
