from __future__ import annotations

from typing import Any, Dict, List, Optional

from .._utils import build_body
from ..types.sending import (
    SendBroadcastResponse,
    SendMessageAcceptedResponse,
    SendMessageBatchResponse,
)
from ._base import BaseResource

MailAddressParam = Dict[str, str]
AttachmentParam = Dict[str, Any]
TrackingParam = Dict[str, bool]


class SendingResource(BaseResource):
    def _sending_headers(
        self,
        channel_id: Optional[str],
        idempotency_key: Optional[str],
    ) -> Optional[Dict[str, str]]:
        headers: Dict[str, str] = {}
        if channel_id is not None:
            headers["X-Helo-Channel-Id"] = channel_id
        if idempotency_key is not None:
            headers["X-Helo-Idempotency-Key"] = idempotency_key
        return headers or None

    def transactional(
        self,
        *,
        from_: MailAddressParam,
        to: List[MailAddressParam],
        cc: Optional[List[MailAddressParam]] = None,
        bcc: Optional[List[MailAddressParam]] = None,
        reply_to: Optional[List[MailAddressParam]] = None,
        subject: Optional[str] = None,
        html: Optional[str] = None,
        text: Optional[str] = None,
        template: Optional[Dict[str, Any]] = None,
        tracking: Optional[TrackingParam] = None,
        attachments: Optional[List[AttachmentParam]] = None,
        tags: Optional[List[str]] = None,
        headers: Optional[Dict[str, str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        channel_id: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> SendMessageAcceptedResponse:
        body: Dict[str, Any] = {"from": from_, "to": to}
        if cc is not None:
            body["cc"] = cc
        if bcc is not None:
            body["bcc"] = bcc
        if reply_to is not None:
            body["replyTo"] = reply_to
        if subject is not None:
            body["subject"] = subject
        if html is not None:
            body["html"] = html
        if text is not None:
            body["text"] = text
        if template is not None:
            body["template"] = template
        if tracking is not None:
            body["tracking"] = tracking
        if attachments is not None:
            body["attachments"] = attachments
        if tags is not None:
            body["tags"] = tags
        if headers is not None:
            body["headers"] = headers
        if metadata is not None:
            body["metadata"] = metadata
        data = self._http.post(
            "/send/transactional",
            json=body,
            headers=self._sending_headers(channel_id, idempotency_key),
        )
        return SendMessageAcceptedResponse.model_validate(data)

    def transactional_batch(
        self,
        *,
        requests: List[Dict[str, Any]],
        channel_id: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> SendMessageBatchResponse:
        data = self._http.post(
            "/send/transactional/batch",
            json={"requests": requests},
            headers=self._sending_headers(channel_id, idempotency_key),
        )
        return SendMessageBatchResponse.model_validate(data)

    def broadcast(
        self,
        *,
        from_: MailAddressParam,
        messages: List[Dict[str, Any]],
        template: Dict[str, Any],
        reply_to: Optional[List[MailAddressParam]] = None,
        tracking: Optional[TrackingParam] = None,
        attachments: Optional[List[AttachmentParam]] = None,
        tags: Optional[List[str]] = None,
        headers: Optional[Dict[str, str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        channel_id: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> SendBroadcastResponse:
        body: Dict[str, Any] = {"from": from_, "messages": messages, "template": template}
        if reply_to is not None:
            body["replyTo"] = reply_to
        if tracking is not None:
            body["tracking"] = tracking
        if attachments is not None:
            body["attachments"] = attachments
        if tags is not None:
            body["tags"] = tags
        if headers is not None:
            body["headers"] = headers
        if metadata is not None:
            body["metadata"] = metadata
        data = self._http.post(
            "/send/broadcast",
            json=body,
            headers=self._sending_headers(channel_id, idempotency_key),
        )
        return SendBroadcastResponse.model_validate(data)

    def broadcast_message(
        self,
        *,
        from_: MailAddressParam,
        to: List[MailAddressParam],
        cc: Optional[List[MailAddressParam]] = None,
        bcc: Optional[List[MailAddressParam]] = None,
        reply_to: Optional[List[MailAddressParam]] = None,
        subject: Optional[str] = None,
        html: Optional[str] = None,
        text: Optional[str] = None,
        template: Optional[Dict[str, Any]] = None,
        tracking: Optional[TrackingParam] = None,
        attachments: Optional[List[AttachmentParam]] = None,
        tags: Optional[List[str]] = None,
        headers: Optional[Dict[str, str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        channel_id: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> SendMessageAcceptedResponse:
        body: Dict[str, Any] = {"from": from_, "to": to}
        if cc is not None:
            body["cc"] = cc
        if bcc is not None:
            body["bcc"] = bcc
        if reply_to is not None:
            body["replyTo"] = reply_to
        if subject is not None:
            body["subject"] = subject
        if html is not None:
            body["html"] = html
        if text is not None:
            body["text"] = text
        if template is not None:
            body["template"] = template
        if tracking is not None:
            body["tracking"] = tracking
        if attachments is not None:
            body["attachments"] = attachments
        if tags is not None:
            body["tags"] = tags
        if headers is not None:
            body["headers"] = headers
        if metadata is not None:
            body["metadata"] = metadata
        data = self._http.post(
            "/send/broadcast/message",
            json=body,
            headers=self._sending_headers(channel_id, idempotency_key),
        )
        return SendMessageAcceptedResponse.model_validate(data)
