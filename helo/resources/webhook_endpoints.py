from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from ..types.params import WebhookHeaderParam
from ..types.shared import WebhookEvent
from ..types.webhook_endpoints import (
    PaginationResultOfWebhookEndpointResponse,
    WebhookEndpointResponse,
)
from ._base import AsyncBaseResource, BaseResource


def _create_body(
    url: str,
    events: Sequence[WebhookEvent],
    channel_id: str | None,
    additional_headers: Sequence[WebhookHeaderParam] | None,
    enabled: bool | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {"url": url, "events": [e.value for e in events]}
    if channel_id is not None:
        body["channelId"] = channel_id
    if additional_headers is not None:
        body["additionalHeaders"] = additional_headers
    if enabled is not None:
        body["enabled"] = enabled
    return body


def _update_body(
    url: str | None,
    events: Sequence[WebhookEvent] | None,
    channel_id: str | None,
    additional_headers: Sequence[WebhookHeaderParam] | None,
    enabled: bool | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {}
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
    return body


def _list_params(
    limit: int | None,
    offset: int | None,
    channel_ids: Sequence[str] | None,
) -> dict[str, Any] | None:
    params: dict[str, Any] = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    if channel_ids is not None:
        params["channelIds"] = ",".join(channel_ids)
    return params or None


class WebhookEndpointsResource(BaseResource):
    def create(
        self,
        *,
        url: str,
        events: Sequence[WebhookEvent],
        channel_id: str | None = None,
        additional_headers: Sequence[WebhookHeaderParam] | None = None,
        enabled: bool | None = None,
    ) -> WebhookEndpointResponse:
        body = _create_body(url, events, channel_id, additional_headers, enabled)
        data = self._http.post("/webhook-endpoints", json=body)
        return WebhookEndpointResponse.model_validate(data)

    def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        channel_ids: Sequence[str] | None = None,
    ) -> PaginationResultOfWebhookEndpointResponse:
        data = self._http.get("/webhook-endpoints", params=_list_params(limit, offset, channel_ids))
        return PaginationResultOfWebhookEndpointResponse.model_validate(data)

    def retrieve(self, id: str) -> WebhookEndpointResponse:
        data = self._http.get(f"/webhook-endpoints/{id}")
        return WebhookEndpointResponse.model_validate(data)

    def update(
        self,
        id: str,
        *,
        url: str | None = None,
        events: Sequence[WebhookEvent] | None = None,
        channel_id: str | None = None,
        additional_headers: Sequence[WebhookHeaderParam] | None = None,
        enabled: bool | None = None,
    ) -> WebhookEndpointResponse:
        body = _update_body(url, events, channel_id, additional_headers, enabled)
        data = self._http.patch(f"/webhook-endpoints/{id}", json=body)
        return WebhookEndpointResponse.model_validate(data)

    def delete(self, id: str) -> None:
        self._http.delete(f"/webhook-endpoints/{id}")

    def regenerate_signing_key(self, id: str) -> WebhookEndpointResponse:
        data = self._http.post(f"/webhook-endpoints/{id}/regenerate-signing-key")
        return WebhookEndpointResponse.model_validate(data)


class AsyncWebhookEndpointsResource(AsyncBaseResource):
    async def create(
        self,
        *,
        url: str,
        events: Sequence[WebhookEvent],
        channel_id: str | None = None,
        additional_headers: Sequence[WebhookHeaderParam] | None = None,
        enabled: bool | None = None,
    ) -> WebhookEndpointResponse:
        body = _create_body(url, events, channel_id, additional_headers, enabled)
        data = await self._http.post("/webhook-endpoints", json=body)
        return WebhookEndpointResponse.model_validate(data)

    async def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        channel_ids: Sequence[str] | None = None,
    ) -> PaginationResultOfWebhookEndpointResponse:
        params = _list_params(limit, offset, channel_ids)
        data = await self._http.get("/webhook-endpoints", params=params)
        return PaginationResultOfWebhookEndpointResponse.model_validate(data)

    async def retrieve(self, id: str) -> WebhookEndpointResponse:
        data = await self._http.get(f"/webhook-endpoints/{id}")
        return WebhookEndpointResponse.model_validate(data)

    async def update(
        self,
        id: str,
        *,
        url: str | None = None,
        events: Sequence[WebhookEvent] | None = None,
        channel_id: str | None = None,
        additional_headers: Sequence[WebhookHeaderParam] | None = None,
        enabled: bool | None = None,
    ) -> WebhookEndpointResponse:
        body = _update_body(url, events, channel_id, additional_headers, enabled)
        data = await self._http.patch(f"/webhook-endpoints/{id}", json=body)
        return WebhookEndpointResponse.model_validate(data)

    async def delete(self, id: str) -> None:
        await self._http.delete(f"/webhook-endpoints/{id}")

    async def regenerate_signing_key(self, id: str) -> WebhookEndpointResponse:
        data = await self._http.post(f"/webhook-endpoints/{id}/regenerate-signing-key")
        return WebhookEndpointResponse.model_validate(data)
