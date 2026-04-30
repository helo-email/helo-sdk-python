from __future__ import annotations

from typing import Any, Dict, List, Optional

from .._utils import build_body
from ..types.shared import WebhookEvent
from ..types.webhook_endpoints import (
    PaginationResultOfWebhookEndpointResponse,
    WebhookEndpointResponse,
    WebhookHeader,
)
from ._base import BaseResource

WebhookHeaderParam = Dict[str, str]


class WebhookEndpointsResource(BaseResource):
    def create(
        self,
        *,
        url: str,
        events: List[WebhookEvent],
        channel_id: Optional[str] = None,
        additional_headers: Optional[List[WebhookHeaderParam]] = None,
        enabled: Optional[bool] = None,
    ) -> WebhookEndpointResponse:
        body: Dict[str, Any] = {"url": url, "events": [e.value for e in events]}
        if channel_id is not None:
            body["channelId"] = channel_id
        if additional_headers is not None:
            body["additionalHeaders"] = additional_headers
        if enabled is not None:
            body["enabled"] = enabled
        data = self._http.post("/webhook-endpoints", json=body)
        return WebhookEndpointResponse.model_validate(data)

    def list(
        self,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        channel_ids: Optional[List[str]] = None,
    ) -> PaginationResultOfWebhookEndpointResponse:
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if channel_ids is not None:
            params["channelIds"] = ",".join(channel_ids)
        data = self._http.get("/webhook-endpoints", params=params or None)
        return PaginationResultOfWebhookEndpointResponse.model_validate(data)

    def retrieve(self, id: str) -> WebhookEndpointResponse:
        data = self._http.get(f"/webhook-endpoints/{id}")
        return WebhookEndpointResponse.model_validate(data)

    def update(
        self,
        id: str,
        *,
        url: Optional[str] = None,
        events: Optional[List[WebhookEvent]] = None,
        channel_id: Optional[str] = None,
        additional_headers: Optional[List[WebhookHeaderParam]] = None,
        enabled: Optional[bool] = None,
    ) -> WebhookEndpointResponse:
        body: Dict[str, Any] = {}
        if url is not None:
            body["url"] = url
        if events is not None:
            body["events"] = [e.value for e in events]
        if channel_id is not None:
            body["channelId"] = channel_id
        if additional_headers is not None:
            body["additionalHeaders"] = additional_headers
        if enabled is not None:
            body["enabled"] = enabled
        data = self._http.patch(f"/webhook-endpoints/{id}", json=body)
        return WebhookEndpointResponse.model_validate(data)

    def delete(self, id: str) -> None:
        self._http.delete(f"/webhook-endpoints/{id}")

    def regenerate_signing_key(self, id: str) -> WebhookEndpointResponse:
        data = self._http.post(f"/webhook-endpoints/{id}/regenerate-signing-key")
        return WebhookEndpointResponse.model_validate(data)
