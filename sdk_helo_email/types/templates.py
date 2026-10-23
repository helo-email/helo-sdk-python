from __future__ import annotations

from datetime import datetime
from typing import Any

from .shared import HeloModel


class CreateTemplateRequest(HeloModel):
    """At least one of html, mjml or text must be supplied. Supplying both html and mjml in the
    same request is rejected - mjml content will be rendered to html. Providing raw html will
    override any mjml content stored on the template.
    """

    name: str
    subject: str
    html: str | None = None
    mjml: str | None = None
    text: str | None = None
    channel_ids: list[str] | None = None


class UpdateTemplateRequest(HeloModel):
    """Only provided fields are changed - an omitted field leaves the existing value unchanged.
    Supplying both html and mjml in the same request is rejected, as is an update that would
    leave the template with no html or text content. Supply version to make the update
    conditional - without it, the last write wins.
    """

    name: str | None = None
    subject: str | None = None
    html: str | None = None
    mjml: str | None = None
    text: str | None = None
    channel_ids: list[str] | None = None
    version: int | None = None


class RenderTemplateRequest(HeloModel):
    inline_styles: bool | None = None
    data: dict[str, Any] | None = None


class RenderDraftRequest(HeloModel):
    """Supplying both html and mjml in the same request is rejected."""

    subject: str
    html: str | None = None
    mjml: str | None = None
    text: str | None = None
    inline_styles: bool | None = None
    data: dict[str, Any] | None = None


class TemplateResponse(HeloModel):
    id: str
    created_at: datetime
    updated_at: datetime
    version: int
    name: str
    subject: str
    html: str | None = None
    mjml: str | None = None
    text: str | None = None
    channel_ids: list[str] | None = None


class TemplateSummaryResponse(HeloModel):
    id: str
    created_at: datetime
    updated_at: datetime
    name: str
    subject: str
    channel_ids: list[str] | None = None


class RenderTemplateResponse(HeloModel):
    subject: str
    html: str | None = None
    text: str | None = None


class PaginatedResponseOfTemplateSummaryResponse(HeloModel):
    total_count: int
    results: list[TemplateSummaryResponse]
