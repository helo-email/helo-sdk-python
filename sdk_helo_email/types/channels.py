from __future__ import annotations

from datetime import datetime

from .shared import DeliveryType, HeloModel


class ChannelTracking(HeloModel):
    links: bool
    opens: bool


class ChannelDetailsResponse(HeloModel):
    id: str | None = None
    name: str | None = None
    delivery_type: DeliveryType | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    tracking: ChannelTracking | None = None


class ChannelBasicResponse(HeloModel):
    id: str | None = None
    name: str | None = None
    delivery_type: DeliveryType | None = None
    created_at: datetime | None = None


class CreateChannelTracking(HeloModel):
    links: bool | None = None
    opens: bool | None = None


class CreateChannelRequest(HeloModel):
    name: str
    delivery_type: DeliveryType
    tracking: CreateChannelTracking | None = None


class PaginationResultOfChannelBasicResponse(HeloModel):
    results: list[ChannelBasicResponse]
    total_count: int


class UpdateChannelTracking(HeloModel):
    links: bool | None = None
    opens: bool | None = None


class UpdateChannelRequest(HeloModel):
    name: str | None = None
    delivery_type: DeliveryType | None = None
    tracking: UpdateChannelTracking | None = None
