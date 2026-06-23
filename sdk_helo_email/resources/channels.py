from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from .._utils import build_body, build_params
from ..types.channels import (
    ChannelDetailsResponse,
    PaginationResultOfChannelBasicResponse,
)
from ..types.params import TrackingParam
from ..types.shared import DeliveryType
from ._base import AsyncBaseResource, BaseResource


def _create_body(
    name: str, delivery_type: DeliveryType, tracking: TrackingParam | None
) -> dict[str, Any]:
    return build_body(name=name, delivery_type=delivery_type.value, tracking=tracking)


def _update_body(
    name: str | None,
    delivery_type: DeliveryType | None,
    tracking: TrackingParam | None,
) -> dict[str, Any]:
    return build_body(
        name=name,
        delivery_type=delivery_type.value if delivery_type else None,
        tracking=tracking,
    )


def _list_params(
    limit: int | None,
    offset: int | None,
    name: str | None,
    channel_ids: Sequence[str] | None,
    delivery_type: DeliveryType | None,
) -> dict[str, Any] | None:
    params = build_params(limit=limit, offset=offset, name=name)
    if channel_ids is not None:
        params["channelIds"] = ",".join(channel_ids)
    if delivery_type is not None:
        params["deliveryType"] = delivery_type.value
    return params or None


class ChannelsResource(BaseResource):
    def create(
        self,
        *,
        name: str,
        delivery_type: DeliveryType,
        tracking: TrackingParam | None = None,
    ) -> ChannelDetailsResponse:
        data = self._http.post("/channels", json=_create_body(name, delivery_type, tracking))
        return ChannelDetailsResponse.model_validate(data)

    def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        name: str | None = None,
        channel_ids: Sequence[str] | None = None,
        delivery_type: DeliveryType | None = None,
    ) -> PaginationResultOfChannelBasicResponse:
        params = _list_params(limit, offset, name, channel_ids, delivery_type)
        data = self._http.get("/channels", params=params)
        return PaginationResultOfChannelBasicResponse.model_validate(data)

    def retrieve(self, id: str) -> ChannelDetailsResponse:
        data = self._http.get(f"/channels/{id}")
        return ChannelDetailsResponse.model_validate(data)

    def update(
        self,
        id: str,
        *,
        name: str | None = None,
        delivery_type: DeliveryType | None = None,
        tracking: TrackingParam | None = None,
    ) -> ChannelDetailsResponse:
        data = self._http.patch(f"/channels/{id}", json=_update_body(name, delivery_type, tracking))
        return ChannelDetailsResponse.model_validate(data)

    def delete(self, id: str) -> None:
        self._http.delete(f"/channels/{id}")


class AsyncChannelsResource(AsyncBaseResource):
    async def create(
        self,
        *,
        name: str,
        delivery_type: DeliveryType,
        tracking: TrackingParam | None = None,
    ) -> ChannelDetailsResponse:
        data = await self._http.post("/channels", json=_create_body(name, delivery_type, tracking))
        return ChannelDetailsResponse.model_validate(data)

    async def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        name: str | None = None,
        channel_ids: Sequence[str] | None = None,
        delivery_type: DeliveryType | None = None,
    ) -> PaginationResultOfChannelBasicResponse:
        params = _list_params(limit, offset, name, channel_ids, delivery_type)
        data = await self._http.get("/channels", params=params)
        return PaginationResultOfChannelBasicResponse.model_validate(data)

    async def retrieve(self, id: str) -> ChannelDetailsResponse:
        data = await self._http.get(f"/channels/{id}")
        return ChannelDetailsResponse.model_validate(data)

    async def update(
        self,
        id: str,
        *,
        name: str | None = None,
        delivery_type: DeliveryType | None = None,
        tracking: TrackingParam | None = None,
    ) -> ChannelDetailsResponse:
        body = _update_body(name, delivery_type, tracking)
        data = await self._http.patch(f"/channels/{id}", json=body)
        return ChannelDetailsResponse.model_validate(data)

    async def delete(self, id: str) -> None:
        await self._http.delete(f"/channels/{id}")
