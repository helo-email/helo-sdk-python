from __future__ import annotations

from typing import Any, Dict, Optional

from ..types.broadcasts import (
    BroadcastDetailsResponse,
    PaginatedResponseOfBroadcast,
    PaginatedResponseOfBroadcastFailure,
    PaginatedResponseOfBroadcastSuppression,
)
from ..types.shared import BroadcastStatus
from ._base import BaseResource


class BroadcastsResource(BaseResource):
    def list(
        self,
        *,
        channel_id: str,
        status: Optional[BroadcastStatus] = None,
        subject: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> PaginatedResponseOfBroadcast:
        params: Dict[str, Any] = {"channelId": channel_id}
        if status is not None:
            params["status"] = status.value
        if subject is not None:
            params["subject"] = subject
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        data = self._http.get("/broadcasts", params=params)
        return PaginatedResponseOfBroadcast.model_validate(data)

    def retrieve(self, id: str) -> BroadcastDetailsResponse:
        data = self._http.get(f"/broadcasts/{id}")
        return BroadcastDetailsResponse.model_validate(data)

    def list_failures(self, id: str) -> PaginatedResponseOfBroadcastFailure:
        data = self._http.get(f"/broadcasts/{id}/failures")
        return PaginatedResponseOfBroadcastFailure.model_validate(data)

    def list_suppressions(self, id: str) -> PaginatedResponseOfBroadcastSuppression:
        data = self._http.get(f"/broadcasts/{id}/suppressions")
        return PaginatedResponseOfBroadcastSuppression.model_validate(data)
