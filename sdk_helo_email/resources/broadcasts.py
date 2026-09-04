from __future__ import annotations

from .._utils import build_params
from ..types.broadcasts import (
    BroadcastDetailsResponse,
    PaginatedResponseOfBroadcast,
    PaginatedResponseOfBroadcastFailure,
    PaginatedResponseOfBroadcastSuppression,
)
from ..types.shared import BroadcastStatus
from ._base import AsyncBaseResource, BaseResource


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
        """List broadcasts"""

        params = build_params(
            channel_id=channel_id,
            status=status.value if status else None,
            subject=subject,
            limit=limit,
            offset=offset,
        )
        data = self._http.get("/broadcasts", params=params)
        return PaginatedResponseOfBroadcast.model_validate(data)

    def retrieve(self, id: str) -> BroadcastDetailsResponse:
        """Retrieve a broadcast"""

        data = self._http.get(f"/broadcasts/{id}")
        return BroadcastDetailsResponse.model_validate(data)

    def list_failures(
        self, id: str, *, limit: int | None = None, offset: int | None = None
    ) -> PaginatedResponseOfBroadcastFailure:
        """List failed broadcast messages"""

        params = build_params(
            limit=limit,
            offset=offset,
        )
        data = self._http.get(f"/broadcasts/{id}/failures", params=params)
        return PaginatedResponseOfBroadcastFailure.model_validate(data)

    def list_suppressions(
        self, id: str, *, limit: int | None = None, offset: int | None = None
    ) -> PaginatedResponseOfBroadcastSuppression:
        """List broadcast suppressed recipients"""

        params = build_params(
            limit=limit,
            offset=offset,
        )
        data = self._http.get(f"/broadcasts/{id}/suppressions", params=params)
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
        """List broadcasts"""

        params = build_params(
            channel_id=channel_id,
            status=status.value if status else None,
            subject=subject,
            limit=limit,
            offset=offset,
        )
        data = await self._http.get("/broadcasts", params=params)
        return PaginatedResponseOfBroadcast.model_validate(data)

    async def retrieve(self, id: str) -> BroadcastDetailsResponse:
        """Retrieve a broadcast"""

        data = await self._http.get(f"/broadcasts/{id}")
        return BroadcastDetailsResponse.model_validate(data)

    async def list_failures(
        self, id: str, *, limit: int | None = None, offset: int | None = None
    ) -> PaginatedResponseOfBroadcastFailure:
        """List failed broadcast messages"""

        params = build_params(
            limit=limit,
            offset=offset,
        )
        data = await self._http.get(f"/broadcasts/{id}/failures", params=params)
        return PaginatedResponseOfBroadcastFailure.model_validate(data)

    async def list_suppressions(
        self, id: str, *, limit: int | None = None, offset: int | None = None
    ) -> PaginatedResponseOfBroadcastSuppression:
        """List broadcast suppressed recipients"""

        params = build_params(
            limit=limit,
            offset=offset,
        )
        data = await self._http.get(f"/broadcasts/{id}/suppressions", params=params)
        return PaginatedResponseOfBroadcastSuppression.model_validate(data)
