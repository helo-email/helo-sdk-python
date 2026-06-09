from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from .._utils import build_params
from ..types.activity import (
    MessageDetailsResponse,
    PaginatedEventsResponse,
    PaginatedMessagesResponse,
)
from ..types.shared import EventType, MailType
from ._base import AsyncBaseResource, BaseResource


def _events_params(
    *,
    channel_id: str | None,
    message_id: str | None,
    after: int | None,
    start_date: str | None,
    end_date: str | None,
    limit: int | None,
    recipient: str | None,
    subject: str | None,
    tags: Sequence[str] | None,
    mail_type: MailType | None,
    event_types: Sequence[EventType] | None,
) -> dict[str, Any] | None:
    params = build_params(
        channel_id=channel_id,
        message_id=message_id,
        after=after,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        recipient=recipient,
        subject=subject,
        tags=tags,
        mail_type=mail_type.value if mail_type else None,
        event_types=[e.value for e in event_types] if event_types else None,
    )
    return params or None


def _messages_params(
    *,
    channel_id: str | None,
    after: int | None,
    start_date: str | None,
    end_date: str | None,
    limit: int | None,
    recipient: str | None,
    subject: str | None,
    tags: Sequence[str] | None,
    mail_type: MailType | None,
    status: str | None,
) -> dict[str, Any] | None:
    params = build_params(
        channel_id=channel_id,
        after=after,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        recipient=recipient,
        subject=subject,
        tags=tags,
        mail_type=mail_type.value if mail_type else None,
        status=status,
    )
    return params or None


class ActivityResource(BaseResource):
    def list_events(
        self,
        *,
        channel_id: str | None = None,
        message_id: str | None = None,
        after: int | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        limit: int | None = None,
        recipient: str | None = None,
        subject: str | None = None,
        tags: Sequence[str] | None = None,
        mail_type: MailType | None = None,
        event_types: Sequence[EventType] | None = None,
    ) -> PaginatedEventsResponse:
        params = _events_params(
            channel_id=channel_id,
            message_id=message_id,
            after=after,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            recipient=recipient,
            subject=subject,
            tags=tags,
            mail_type=mail_type,
            event_types=event_types,
        )
        data = self._http.get("/activity/events", params=params)
        return PaginatedEventsResponse.model_validate(data)

    def list_messages(
        self,
        *,
        channel_id: str | None = None,
        after: int | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        limit: int | None = None,
        recipient: str | None = None,
        subject: str | None = None,
        tags: Sequence[str] | None = None,
        mail_type: MailType | None = None,
        status: str | None = None,
    ) -> PaginatedMessagesResponse:
        params = _messages_params(
            channel_id=channel_id,
            after=after,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            recipient=recipient,
            subject=subject,
            tags=tags,
            mail_type=mail_type,
            status=status,
        )
        data = self._http.get("/activity/messages", params=params)
        return PaginatedMessagesResponse.model_validate(data)

    def retrieve_message(self, id: str) -> MessageDetailsResponse:
        data = self._http.get(f"/activity/messages/{id}")
        return MessageDetailsResponse.model_validate(data)


class AsyncActivityResource(AsyncBaseResource):
    async def list_events(
        self,
        *,
        channel_id: str | None = None,
        message_id: str | None = None,
        after: int | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        limit: int | None = None,
        recipient: str | None = None,
        subject: str | None = None,
        tags: Sequence[str] | None = None,
        mail_type: MailType | None = None,
        event_types: Sequence[EventType] | None = None,
    ) -> PaginatedEventsResponse:
        params = _events_params(
            channel_id=channel_id,
            message_id=message_id,
            after=after,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            recipient=recipient,
            subject=subject,
            tags=tags,
            mail_type=mail_type,
            event_types=event_types,
        )
        data = await self._http.get("/activity/events", params=params)
        return PaginatedEventsResponse.model_validate(data)

    async def list_messages(
        self,
        *,
        channel_id: str | None = None,
        after: int | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        limit: int | None = None,
        recipient: str | None = None,
        subject: str | None = None,
        tags: Sequence[str] | None = None,
        mail_type: MailType | None = None,
        status: str | None = None,
    ) -> PaginatedMessagesResponse:
        params = _messages_params(
            channel_id=channel_id,
            after=after,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            recipient=recipient,
            subject=subject,
            tags=tags,
            mail_type=mail_type,
            status=status,
        )
        data = await self._http.get("/activity/messages", params=params)
        return PaginatedMessagesResponse.model_validate(data)

    async def retrieve_message(self, id: str) -> MessageDetailsResponse:
        data = await self._http.get(f"/activity/messages/{id}")
        return MessageDetailsResponse.model_validate(data)
