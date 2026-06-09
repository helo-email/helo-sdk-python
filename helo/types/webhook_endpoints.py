from __future__ import annotations

from .shared import HeloModel, WebhookEvent


class WebhookHeader(HeloModel):
    name: str
    value: str


class WebhookEndpointResponse(HeloModel):
    id: str | None = None
    channel_id: str | None = None
    url: str | None = None
    payload_signing_key: str | None = None
    enabled: bool | None = None
    additional_headers: list[WebhookHeader] | None = None
    events: list[WebhookEvent] | None = None


class PaginationResultOfWebhookEndpointResponse(HeloModel):
    results: list[WebhookEndpointResponse]
    total_count: int
