from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from ..types.shared import MailType, SuppressionReason
from ..types.suppressions import (
    CreateSuppressionsResponse,
    PaginatedResponseOfSuppressionResponse,
    RemoveSuppressionsResponse,
)
from ._base import AsyncBaseResource, BaseResource


def _list_params(
    channel_id: str,
    mail_type: MailType,
    reason: SuppressionReason | None,
    email: str | None,
    limit: int | None,
    offset: int | None,
) -> dict[str, Any]:
    params: dict[str, Any] = {"channelId": channel_id, "mailType": mail_type.value}
    if reason is not None:
        params["reason"] = reason.value
    if email is not None:
        params["email"] = email
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    return params


def _mutation_body(channel_id: str, mail_type: MailType, emails: Sequence[str]) -> dict[str, Any]:
    return {"channelId": channel_id, "mailType": mail_type.value, "emails": emails}


class SuppressionsResource(BaseResource):
    def list(
        self,
        *,
        channel_id: str,
        mail_type: MailType,
        reason: SuppressionReason | None = None,
        email: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> PaginatedResponseOfSuppressionResponse:
        params = _list_params(channel_id, mail_type, reason, email, limit, offset)
        data = self._http.get("/suppressions", params=params)
        return PaginatedResponseOfSuppressionResponse.model_validate(data)

    def create(
        self,
        *,
        channel_id: str,
        mail_type: MailType,
        emails: Sequence[str],
    ) -> CreateSuppressionsResponse:
        body = _mutation_body(channel_id, mail_type, emails)
        data = self._http.post("/suppressions", json=body)
        return CreateSuppressionsResponse.model_validate(data)

    def remove(
        self,
        *,
        channel_id: str,
        mail_type: MailType,
        emails: Sequence[str],
    ) -> RemoveSuppressionsResponse:
        body = _mutation_body(channel_id, mail_type, emails)
        data = self._http.post("/suppressions/remove", json=body)
        return RemoveSuppressionsResponse.model_validate(data)


class AsyncSuppressionsResource(AsyncBaseResource):
    async def list(
        self,
        *,
        channel_id: str,
        mail_type: MailType,
        reason: SuppressionReason | None = None,
        email: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> PaginatedResponseOfSuppressionResponse:
        params = _list_params(channel_id, mail_type, reason, email, limit, offset)
        data = await self._http.get("/suppressions", params=params)
        return PaginatedResponseOfSuppressionResponse.model_validate(data)

    async def create(
        self,
        *,
        channel_id: str,
        mail_type: MailType,
        emails: Sequence[str],
    ) -> CreateSuppressionsResponse:
        body = _mutation_body(channel_id, mail_type, emails)
        data = await self._http.post("/suppressions", json=body)
        return CreateSuppressionsResponse.model_validate(data)

    async def remove(
        self,
        *,
        channel_id: str,
        mail_type: MailType,
        emails: Sequence[str],
    ) -> RemoveSuppressionsResponse:
        body = _mutation_body(channel_id, mail_type, emails)
        data = await self._http.post("/suppressions/remove", json=body)
        return RemoveSuppressionsResponse.model_validate(data)
