from __future__ import annotations

from collections.abc import Sequence

from .._utils import build_params
from ..types.activity import (
    MessageDetailsResponse,
    PaginatedEventsResponse,
    PaginatedMessagesResponse,
)
from ..types.shared import EventType, MailType, MessageStatus
from ._base import AsyncBaseResource, BaseResource


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
        """List activity events"""

        params = build_params(
            channel_id=channel_id,
            message_id=message_id,
            after=after,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            recipient=recipient,
            subject=subject,
            tags=",".join(tags) if tags else None,
            mail_type=mail_type.value if mail_type else None,
            event_types=",".join([item.value for item in event_types]) if event_types else None,
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
        status: MessageStatus | None = None,
    ) -> PaginatedMessagesResponse:
        """List messages"""

        params = build_params(
            channel_id=channel_id,
            after=after,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            recipient=recipient,
            subject=subject,
            tags=",".join(tags) if tags else None,
            mail_type=mail_type.value if mail_type else None,
            status=status.value if status else None,
        )
        data = self._http.get("/activity/messages", params=params)
        return PaginatedMessagesResponse.model_validate(data)

    def retrieve_message(self, id: str) -> MessageDetailsResponse:
        """Retrieve message details"""

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
        """List activity events"""

        params = build_params(
            channel_id=channel_id,
            message_id=message_id,
            after=after,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            recipient=recipient,
            subject=subject,
            tags=",".join(tags) if tags else None,
            mail_type=mail_type.value if mail_type else None,
            event_types=",".join([item.value for item in event_types]) if event_types else None,
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
        status: MessageStatus | None = None,
    ) -> PaginatedMessagesResponse:
        """List messages"""

        params = build_params(
            channel_id=channel_id,
            after=after,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            recipient=recipient,
            subject=subject,
            tags=",".join(tags) if tags else None,
            mail_type=mail_type.value if mail_type else None,
            status=status.value if status else None,
        )
        data = await self._http.get("/activity/messages", params=params)
        return PaginatedMessagesResponse.model_validate(data)

    async def retrieve_message(self, id: str) -> MessageDetailsResponse:
        """Retrieve message details"""

        data = await self._http.get(f"/activity/messages/{id}")
        return MessageDetailsResponse.model_validate(data)
