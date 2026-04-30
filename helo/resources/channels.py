from __future__ import annotations

from typing import Any, Dict, List, Optional

from .._utils import build_body, build_params
from ..types.channels import (
    ChannelDetailsResponse,
    PaginationResultOfChannelBasicResponse,
)
from ..types.shared import DeliveryType
from ._base import BaseResource


class ChannelsResource(BaseResource):
    def create(
        self,
        *,
        name: str,
        delivery_type: DeliveryType,
        tracking: Optional[Dict[str, bool]] = None,
    ) -> ChannelDetailsResponse:
        body = build_body(name=name, delivery_type=delivery_type.value, tracking=tracking)
        data = self._http.post("/channels", json=body)
        return ChannelDetailsResponse.model_validate(data)

    def list(
        self,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        name: Optional[str] = None,
        channel_ids: Optional[List[str]] = None,
        delivery_type: Optional[DeliveryType] = None,
    ) -> PaginationResultOfChannelBasicResponse:
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if name is not None:
            params["name"] = name
        if channel_ids is not None:
            params["channelIds"] = ",".join(channel_ids)
        if delivery_type is not None:
            params["deliveryType"] = delivery_type.value
        data = self._http.get("/channels", params=params or None)
        return PaginationResultOfChannelBasicResponse.model_validate(data)

    def retrieve(self, id: str) -> ChannelDetailsResponse:
        data = self._http.get(f"/channels/{id}")
        return ChannelDetailsResponse.model_validate(data)

    def update(
        self,
        id: str,
        *,
        name: Optional[str] = None,
        delivery_type: Optional[DeliveryType] = None,
        tracking: Optional[Dict[str, bool]] = None,
    ) -> ChannelDetailsResponse:
        body = build_body(
            name=name,
            delivery_type=delivery_type.value if delivery_type else None,
            tracking=tracking,
        )
        data = self._http.patch(f"/channels/{id}", json=body)
        return ChannelDetailsResponse.model_validate(data)

    def delete(self, id: str) -> None:
        self._http.delete(f"/channels/{id}")
