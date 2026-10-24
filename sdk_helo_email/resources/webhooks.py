from __future__ import annotations

from collections.abc import Sequence

from .._utils import build_body, build_params
from ..types.params import WebhookHeaderParam
from ..types.shared import WebhookEvent
from ..types.webhooks import PaginationResultOfWebhookResponse, WebhookResponse
from ._base import AsyncBaseResource, BaseResource


class WebhooksResource(BaseResource):
    def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        channel_ids: Sequence[str] | None = None,
    ) -> PaginationResultOfWebhookResponse:
        """List all webhooks"""

        params = build_params(
            limit=limit,
            offset=offset,
            channel_ids=",".join(channel_ids) if channel_ids else None,
        )
        data = self._http.get("/webhooks", params=params)
        return PaginationResultOfWebhookResponse.model_validate(data)

    def create(
        self,
        *,
        url: str,
        events: Sequence[WebhookEvent],
        channel_id: str | None = None,
        additional_headers: Sequence[WebhookHeaderParam] | None = None,
        enabled: bool | None = None,
    ) -> WebhookResponse:
        """Create a webhook"""

        body = build_body(
            url=url,
            events=[item.value for item in events] if events else None,
            channel_id=channel_id,
            additional_headers=[str(item) for item in additional_headers]
            if additional_headers
            else None,
            enabled=enabled,
        )
        data = self._http.post("/webhooks", json=body)
        return WebhookResponse.model_validate(data)

    def retrieve(self, id: str) -> WebhookResponse:
        """Retrieve a webhook"""

        data = self._http.get(f"/webhooks/{id}")
        return WebhookResponse.model_validate(data)

    def update(
        self,
        id: str,
        *,
        url: str | None = None,
        events: Sequence[WebhookEvent] | None = None,
        channel_id: str | None = None,
        additional_headers: Sequence[WebhookHeaderParam] | None = None,
        enabled: bool | None = None,
    ) -> WebhookResponse:
        """Update a webhook"""

        body = build_body(
            url=url,
            events=[item.value for item in events] if events else None,
            channel_id=channel_id,
            additional_headers=[str(item) for item in additional_headers]
            if additional_headers
            else None,
            enabled=enabled,
        )
        data = self._http.patch(f"/webhooks/{id}", json=body)
        return WebhookResponse.model_validate(data)

    def delete(self, id: str) -> None:
        """Delete a webhook"""

        self._http.delete(f"/webhooks/{id}")

    def regenerate_signing_key(self, id: str) -> WebhookResponse:
        """Regenerate webhook signing key"""

        data = self._http.post(f"/webhooks/{id}/regenerate-signing-key")
        return WebhookResponse.model_validate(data)


class AsyncWebhooksResource(AsyncBaseResource):
    async def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        channel_ids: Sequence[str] | None = None,
    ) -> PaginationResultOfWebhookResponse:
        """List all webhooks"""

        params = build_params(
            limit=limit,
            offset=offset,
            channel_ids=",".join(channel_ids) if channel_ids else None,
        )
        data = await self._http.get("/webhooks", params=params)
        return PaginationResultOfWebhookResponse.model_validate(data)

    async def create(
        self,
        *,
        url: str,
        events: Sequence[WebhookEvent],
        channel_id: str | None = None,
        additional_headers: Sequence[WebhookHeaderParam] | None = None,
        enabled: bool | None = None,
    ) -> WebhookResponse:
        """Create a webhook"""

        body = build_body(
            url=url,
            events=[item.value for item in events] if events else None,
            channel_id=channel_id,
            additional_headers=[str(item) for item in additional_headers]
            if additional_headers
            else None,
            enabled=enabled,
        )
        data = await self._http.post("/webhooks", json=body)
        return WebhookResponse.model_validate(data)

    async def retrieve(self, id: str) -> WebhookResponse:
        """Retrieve a webhook"""

        data = await self._http.get(f"/webhooks/{id}")
        return WebhookResponse.model_validate(data)

    async def update(
        self,
        id: str,
        *,
        url: str | None = None,
        events: Sequence[WebhookEvent] | None = None,
        channel_id: str | None = None,
        additional_headers: Sequence[WebhookHeaderParam] | None = None,
        enabled: bool | None = None,
    ) -> WebhookResponse:
        """Update a webhook"""

        body = build_body(
            url=url,
            events=[item.value for item in events] if events else None,
            channel_id=channel_id,
            additional_headers=[str(item) for item in additional_headers]
            if additional_headers
            else None,
            enabled=enabled,
        )
        data = await self._http.patch(f"/webhooks/{id}", json=body)
        return WebhookResponse.model_validate(data)

    async def delete(self, id: str) -> None:
        """Delete a webhook"""

        await self._http.delete(f"/webhooks/{id}")

    async def regenerate_signing_key(self, id: str) -> WebhookResponse:
        """Regenerate webhook signing key"""

        data = await self._http.post(f"/webhooks/{id}/regenerate-signing-key")
        return WebhookResponse.model_validate(data)
