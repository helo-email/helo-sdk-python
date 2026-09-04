from __future__ import annotations

from collections.abc import Sequence

from .._utils import build_body, build_params
from ..types.shared import MailType, SuppressionReason
from ..types.suppressions import (
    CreateSuppressionsResponse,
    PaginatedResponseOfSuppressionResponse,
    RemoveSuppressionsResponse,
)
from ._base import AsyncBaseResource, BaseResource


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
        """List suppressions"""

        params = build_params(
            channel_id=channel_id,
            mail_type=mail_type.value,
            reason=reason.value if reason else None,
            email=email,
            limit=limit,
            offset=offset,
        )
        data = self._http.get("/suppressions", params=params)
        return PaginatedResponseOfSuppressionResponse.model_validate(data)

    def create(
        self, *, channel_id: str, mail_type: MailType, emails: Sequence[str]
    ) -> CreateSuppressionsResponse:
        """Create suppressions"""

        body = build_body(
            channel_id=channel_id,
            mail_type=mail_type.value,
            emails=emails if emails else None,
        )
        data = self._http.post("/suppressions", json=body)
        return CreateSuppressionsResponse.model_validate(data)

    def remove(
        self, *, channel_id: str, mail_type: MailType, emails: Sequence[str]
    ) -> RemoveSuppressionsResponse:
        """Remove suppressions"""

        body = build_body(
            channel_id=channel_id,
            mail_type=mail_type.value,
            emails=emails if emails else None,
        )
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
        """List suppressions"""

        params = build_params(
            channel_id=channel_id,
            mail_type=mail_type.value,
            reason=reason.value if reason else None,
            email=email,
            limit=limit,
            offset=offset,
        )
        data = await self._http.get("/suppressions", params=params)
        return PaginatedResponseOfSuppressionResponse.model_validate(data)

    async def create(
        self, *, channel_id: str, mail_type: MailType, emails: Sequence[str]
    ) -> CreateSuppressionsResponse:
        """Create suppressions"""

        body = build_body(
            channel_id=channel_id,
            mail_type=mail_type.value,
            emails=emails if emails else None,
        )
        data = await self._http.post("/suppressions", json=body)
        return CreateSuppressionsResponse.model_validate(data)

    async def remove(
        self, *, channel_id: str, mail_type: MailType, emails: Sequence[str]
    ) -> RemoveSuppressionsResponse:
        """Remove suppressions"""

        body = build_body(
            channel_id=channel_id,
            mail_type=mail_type.value,
            emails=emails if emails else None,
        )
        data = await self._http.post("/suppressions/remove", json=body)
        return RemoveSuppressionsResponse.model_validate(data)
