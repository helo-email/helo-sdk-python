from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from .shared import DeliveryType, HeloModel


class ChannelTracking(HeloModel):
    links: bool
    opens: bool


class ChannelDetailsResponse(HeloModel):
    id: str
    name: str
    delivery_type: DeliveryType
    created_at: datetime
    updated_at: datetime
    tracking: ChannelTracking


class ChannelBasicResponse(HeloModel):
    id: str
    name: str
    delivery_type: DeliveryType
    created_at: datetime


class PaginationResultOfChannelBasicResponse(HeloModel):
    results: List[ChannelBasicResponse]
    total_count: int
