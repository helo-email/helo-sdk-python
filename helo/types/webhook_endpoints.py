from __future__ import annotations

from typing import List, Optional

from .shared import HeloModel, WebhookEvent


class WebhookHeader(HeloModel):
    name: str
    value: str


class WebhookEndpointResponse(HeloModel):
    id: Optional[str] = None
    channel_id: Optional[str] = None
    url: Optional[str] = None
    payload_signing_key: Optional[str] = None
    enabled: Optional[bool] = None
    additional_headers: Optional[List[WebhookHeader]] = None
    events: Optional[List[WebhookEvent]] = None


class PaginationResultOfWebhookEndpointResponse(HeloModel):
    results: List[WebhookEndpointResponse]
    total_count: int
