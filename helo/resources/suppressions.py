from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..types.shared import MailType, SuppressionReason
from ..types.suppressions import (
    CreateSuppressionsResponse,
    PaginatedResponseOfSuppressionResponse,
    RemoveSuppressionsResponse,
)
from ._base import BaseResource


class SuppressionsResource(BaseResource):
    def list(
        self,
        *,
        channel_id: str,
        mail_type: MailType,
        reason: Optional[SuppressionReason] = None,
        email: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> PaginatedResponseOfSuppressionResponse:
        params: Dict[str, Any] = {
            "channelId": channel_id,
            "mailType": mail_type.value,
        }
        if reason is not None:
            params["reason"] = reason.value
        if email is not None:
            params["email"] = email
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        data = self._http.get("/suppressions", params=params)
        return PaginatedResponseOfSuppressionResponse.model_validate(data)

    def create(
        self,
        *,
        channel_id: str,
        mail_type: MailType,
        emails: List[str],
    ) -> CreateSuppressionsResponse:
        body = {
            "channelId": channel_id,
            "mailType": mail_type.value,
            "emails": emails,
        }
        data = self._http.post("/suppressions", json=body)
        return CreateSuppressionsResponse.model_validate(data)

    def remove(
        self,
        *,
        channel_id: str,
        mail_type: MailType,
        emails: List[str],
    ) -> RemoveSuppressionsResponse:
        body = {
            "channelId": channel_id,
            "mailType": mail_type.value,
            "emails": emails,
        }
        data = self._http.post("/suppressions/remove", json=body)
        return RemoveSuppressionsResponse.model_validate(data)
