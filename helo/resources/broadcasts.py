from __future__ import annotations

from typing import Any

from ..types.broadcasts import (
    BroadcastDetailsResponse,
    PaginatedResponseOfBroadcast,
    PaginatedResponseOfBroadcastFailure,
    PaginatedResponseOfBroadcastSuppression,
)
from ..types.shared import BroadcastStatus
from ._base import AsyncBaseResource, BaseResource


def _list_params(
    channel_id: str,
    status: BroadcastStatus | None,
    subject: str | None,
    limit: int | None,
    offset: int | None,
) -> dict[str, Any]:
    params: dict[str, Any] = {"channelId": channel_id}
    if status is not None:
        params["status"] = status.value
    if subject is not None:
        params["subject"] = subject
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    return params


class BroadcastsResource(BaseResource):
    def list(
        self,
        *,
        channel_id: str,
        status: BroadcastStatus | None = None,
        subject: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> PaginatedResponseOfBroadcast:
        params = _list_params(channel_id, status, subject, limit, offset)
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


class AsyncBroadcastsResource(AsyncBaseResource):
    async def list(
        self,
        *,
        channel_id: str,
        status: BroadcastStatus | None = None,
        subject: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> PaginatedResponseOfBroadcast:
        params = _list_params(channel_id, status, subject, limit, offset)
        data = await self._http.get("/broadcasts", params=params)
        return PaginatedResponseOfBroadcast.model_validate(data)

    async def retrieve(self, id: str) -> BroadcastDetailsResponse:
        data = await self._http.get(f"/broadcasts/{id}")
        return BroadcastDetailsResponse.model_validate(data)

    async def list_failures(self, id: str) -> PaginatedResponseOfBroadcastFailure:
        data = await self._http.get(f"/broadcasts/{id}/failures")
        return PaginatedResponseOfBroadcastFailure.model_validate(data)

    async def list_suppressions(self, id: str) -> PaginatedResponseOfBroadcastSuppression:
        data = await self._http.get(f"/broadcasts/{id}/suppressions")
        return PaginatedResponseOfBroadcastSuppression.model_validate(data)
