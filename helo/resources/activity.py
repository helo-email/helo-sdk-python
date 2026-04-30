from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..types.activity import (
    MessageDetailsResponse,
    PaginatedEventsResponse,
    PaginatedMessagesResponse,
)
from ..types.shared import EventType, MailType
from ._base import BaseResource


class ActivityResource(BaseResource):
    def list_events(
        self,
        *,
        channel_id: Optional[str] = None,
        message_id: Optional[str] = None,
        after: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: Optional[int] = None,
        recipient: Optional[str] = None,
        subject: Optional[str] = None,
        tags: Optional[List[str]] = None,
        mail_type: Optional[MailType] = None,
        event_types: Optional[List[EventType]] = None,
    ) -> PaginatedEventsResponse:
        params: Dict[str, Any] = {}
        if channel_id is not None:
            params["channelId"] = channel_id
        if message_id is not None:
            params["messageId"] = message_id
        if after is not None:
            params["after"] = after
        if start_date is not None:
            params["startDate"] = start_date
        if end_date is not None:
            params["endDate"] = end_date
        if limit is not None:
            params["limit"] = limit
        if recipient is not None:
            params["recipient"] = recipient
        if subject is not None:
            params["subject"] = subject
        if tags is not None:
            params["tags"] = tags
        if mail_type is not None:
            params["mailType"] = mail_type.value
        if event_types is not None:
            params["eventTypes"] = [e.value for e in event_types]
        data = self._http.get("/activity/events", params=params or None)
        return PaginatedEventsResponse.model_validate(data)

    def list_messages(
        self,
        *,
        channel_id: Optional[str] = None,
        after: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: Optional[int] = None,
        recipient: Optional[str] = None,
        subject: Optional[str] = None,
        tags: Optional[List[str]] = None,
        mail_type: Optional[MailType] = None,
        status: Optional[str] = None,
    ) -> PaginatedMessagesResponse:
        params: Dict[str, Any] = {}
        if channel_id is not None:
            params["channelId"] = channel_id
        if after is not None:
            params["after"] = after
        if start_date is not None:
            params["startDate"] = start_date
        if end_date is not None:
            params["endDate"] = end_date
        if limit is not None:
            params["limit"] = limit
        if recipient is not None:
            params["recipient"] = recipient
        if subject is not None:
            params["subject"] = subject
        if tags is not None:
            params["tags"] = tags
        if mail_type is not None:
            params["mailType"] = mail_type.value
        if status is not None:
            params["status"] = status
        data = self._http.get("/activity/messages", params=params or None)
        return PaginatedMessagesResponse.model_validate(data)

    def retrieve_message(self, id: str) -> MessageDetailsResponse:
        data = self._http.get(f"/activity/messages/{id}")
        return MessageDetailsResponse.model_validate(data)
