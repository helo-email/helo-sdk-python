from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from .._utils import build_body, build_params
from ..types.templates import PaginatedResponseOfTemplateSummaryResponse, RenderTemplateResponse, TemplateResponse
from ._base import AsyncBaseResource, BaseResource


class TemplatesResource(BaseResource):
    def list(self, *, limit: int | None = None, offset: int | None = None, name: str | None = None, channel_ids: Sequence[str] | None = None) -> PaginatedResponseOfTemplateSummaryResponse:
        params = build_params(
            limit=limit,
            offset=offset,
            name=name,
            channel_ids=",".join(channel_ids) if channel_ids else None,
        )
        data = self._http.get("/templates", params=params)
        return PaginatedResponseOfTemplateSummaryResponse.model_validate(data)

    def create(self, *, name: str, subject: str, html: str | None = None, mjml: str | None = None, text: str | None = None, channel_ids: Sequence[str] | None = None) -> TemplateResponse:
        body = build_body(
            name=name,
            subject=subject,
            html=html,
            mjml=mjml,
            text=text,
            channel_ids=channel_ids if channel_ids else None,
        )
        data = self._http.post("/templates", json=body)
        return TemplateResponse.model_validate(data)

    def render_draft(self, *, subject: str, html: str | None = None, mjml: str | None = None, text: str | None = None, inline_styles: bool | None = None, data: dict[str, Any] | None = None) -> RenderTemplateResponse:
        body = build_body(
            subject=subject,
            html=html,
            mjml=mjml,
            text=text,
            inline_styles=inline_styles,
            data=data,
        )
        data = self._http.post("/templates/render", json=body)
        return RenderTemplateResponse.model_validate(data)

    def retrieve(self, id: str) -> TemplateResponse:
        data = self._http.get(f"/templates/{id}")
        return TemplateResponse.model_validate(data)

    def update(self, id: str, *, name: str | None = None, subject: str | None = None, html: str | None = None, mjml: str | None = None, text: str | None = None, channel_ids: Sequence[str] | None = None, version: int | None = None) -> TemplateResponse:
        body = build_body(
            name=name,
            subject=subject,
            html=html,
            mjml=mjml,
            text=text,
            channel_ids=channel_ids if channel_ids else None,
            version=version,
        )
        data = self._http.patch(f"/templates/{id}", json=body)
        return TemplateResponse.model_validate(data)

    def delete(self, id: str) -> None:
        self._http.delete(f"/templates/{id}")

    def render(self, id: str, *, inline_styles: bool | None = None, data: dict[str, Any] | None = None) -> RenderTemplateResponse:
        body = build_body(
            inline_styles=inline_styles,
            data=data,
        )
        data = self._http.post(f"/templates/{id}/render", json=body)
        return RenderTemplateResponse.model_validate(data)


class AsyncTemplatesResource(AsyncBaseResource):
    async def list(self, *, limit: int | None = None, offset: int | None = None, name: str | None = None, channel_ids: Sequence[str] | None = None) -> PaginatedResponseOfTemplateSummaryResponse:
        params = build_params(
            limit=limit,
            offset=offset,
            name=name,
            channel_ids=",".join(channel_ids) if channel_ids else None,
        )
        data = await self._http.get("/templates", params=params)
        return PaginatedResponseOfTemplateSummaryResponse.model_validate(data)

    async def create(self, *, name: str, subject: str, html: str | None = None, mjml: str | None = None, text: str | None = None, channel_ids: Sequence[str] | None = None) -> TemplateResponse:
        body = build_body(
            name=name,
            subject=subject,
            html=html,
            mjml=mjml,
            text=text,
            channel_ids=channel_ids if channel_ids else None,
        )
        data = await self._http.post("/templates", json=body)
        return TemplateResponse.model_validate(data)

    async def render_draft(self, *, subject: str, html: str | None = None, mjml: str | None = None, text: str | None = None, inline_styles: bool | None = None, data: dict[str, Any] | None = None) -> RenderTemplateResponse:
        body = build_body(
            subject=subject,
            html=html,
            mjml=mjml,
            text=text,
            inline_styles=inline_styles,
            data=data,
        )
        data = await self._http.post("/templates/render", json=body)
        return RenderTemplateResponse.model_validate(data)

    async def retrieve(self, id: str) -> TemplateResponse:
        data = await self._http.get(f"/templates/{id}")
        return TemplateResponse.model_validate(data)

    async def update(self, id: str, *, name: str | None = None, subject: str | None = None, html: str | None = None, mjml: str | None = None, text: str | None = None, channel_ids: Sequence[str] | None = None, version: int | None = None) -> TemplateResponse:
        body = build_body(
            name=name,
            subject=subject,
            html=html,
            mjml=mjml,
            text=text,
            channel_ids=channel_ids if channel_ids else None,
            version=version,
        )
        data = await self._http.patch(f"/templates/{id}", json=body)
        return TemplateResponse.model_validate(data)

    async def delete(self, id: str) -> None:
        await self._http.delete(f"/templates/{id}")

    async def render(self, id: str, *, inline_styles: bool | None = None, data: dict[str, Any] | None = None) -> RenderTemplateResponse:
        body = build_body(
            inline_styles=inline_styles,
            data=data,
        )
        data = await self._http.post(f"/templates/{id}/render", json=body)
        return RenderTemplateResponse.model_validate(data)
