from __future__ import annotations

from collections.abc import Sequence

from .._utils import build_body, build_params
from ..types.channels import ChannelDetailsResponse, PaginationResultOfChannelBasicResponse
from ..types.params import CreateChannelTrackingParam, UpdateChannelTrackingParam
from ..types.shared import DeliveryType
from ._base import AsyncBaseResource, BaseResource


class ChannelsResource(BaseResource):
    def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        name: str | None = None,
        channel_ids: Sequence[str] | None = None,
        delivery_type: DeliveryType | None = None,
    ) -> PaginationResultOfChannelBasicResponse:
        """List all channels"""

        params = build_params(
            limit=limit,
            offset=offset,
            name=name,
            channel_ids=",".join(channel_ids) if channel_ids else None,
            delivery_type=delivery_type.value if delivery_type else None,
        )
        data = self._http.get("/channels", params=params)
        return PaginationResultOfChannelBasicResponse.model_validate(data)

    def create(
        self,
        *,
        name: str,
        delivery_type: DeliveryType,
        tracking: CreateChannelTrackingParam | None = None,
    ) -> ChannelDetailsResponse:
        """Create a channel"""

        body = build_body(
            name=name,
            delivery_type=delivery_type.value,
            tracking=tracking,
        )
        data = self._http.post("/channels", json=body)
        return ChannelDetailsResponse.model_validate(data)

    def retrieve(self, id: str) -> ChannelDetailsResponse:
        """Retrieve a channel"""

        data = self._http.get(f"/channels/{id}")
        return ChannelDetailsResponse.model_validate(data)

    def update(
        self,
        id: str,
        *,
        name: str | None = None,
        delivery_type: DeliveryType | None = None,
        tracking: UpdateChannelTrackingParam | None = None,
    ) -> ChannelDetailsResponse:
        """Update a channel"""

        body = build_body(
            name=name,
            delivery_type=delivery_type.value if delivery_type else None,
            tracking=tracking,
        )
        data = self._http.patch(f"/channels/{id}", json=body)
        return ChannelDetailsResponse.model_validate(data)

    def delete(self, id: str) -> None:
        """Delete a channel"""

        self._http.delete(f"/channels/{id}")


class AsyncChannelsResource(AsyncBaseResource):
    async def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        name: str | None = None,
        channel_ids: Sequence[str] | None = None,
        delivery_type: DeliveryType | None = None,
    ) -> PaginationResultOfChannelBasicResponse:
        """List all channels"""

        params = build_params(
            limit=limit,
            offset=offset,
            name=name,
            channel_ids=",".join(channel_ids) if channel_ids else None,
            delivery_type=delivery_type.value if delivery_type else None,
        )
        data = await self._http.get("/channels", params=params)
        return PaginationResultOfChannelBasicResponse.model_validate(data)

    async def create(
        self,
        *,
        name: str,
        delivery_type: DeliveryType,
        tracking: CreateChannelTrackingParam | None = None,
    ) -> ChannelDetailsResponse:
        """Create a channel"""

        body = build_body(
            name=name,
            delivery_type=delivery_type.value,
            tracking=tracking,
        )
        data = await self._http.post("/channels", json=body)
        return ChannelDetailsResponse.model_validate(data)

    async def retrieve(self, id: str) -> ChannelDetailsResponse:
        """Retrieve a channel"""

        data = await self._http.get(f"/channels/{id}")
        return ChannelDetailsResponse.model_validate(data)

    async def update(
        self,
        id: str,
        *,
        name: str | None = None,
        delivery_type: DeliveryType | None = None,
        tracking: UpdateChannelTrackingParam | None = None,
    ) -> ChannelDetailsResponse:
        """Update a channel"""

        body = build_body(
            name=name,
            delivery_type=delivery_type.value if delivery_type else None,
            tracking=tracking,
        )
        data = await self._http.patch(f"/channels/{id}", json=body)
        return ChannelDetailsResponse.model_validate(data)

    async def delete(self, id: str) -> None:
        """Delete a channel"""

        await self._http.delete(f"/channels/{id}")
