from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from .._utils import build_body, build_params
from ..types.domains import (
    DnsRecordResponse,
    DnsRecordsResponse,
    DomainResponse,
    DomainWithDnsResponse,
    PaginatedResponseOfDomainResponse,
)
from ._base import AsyncBaseResource, BaseResource


def _list_params(
    limit: int | None,
    offset: int | None,
    name: str | None,
    channel_ids: Sequence[str] | None,
) -> dict[str, Any] | None:
    params = build_params(limit=limit, offset=offset, name=name)
    if channel_ids is not None:
        params["channelIds"] = ",".join(channel_ids)
    return params or None


class DomainsResource(BaseResource):
    def create(
        self,
        *,
        name: str,
        channel_ids: Sequence[str] | None = None,
    ) -> DomainWithDnsResponse:
        data = self._http.post("/domains", json=build_body(name=name, channel_ids=channel_ids))
        return DomainWithDnsResponse.model_validate(data)

    def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        name: str | None = None,
        channel_ids: Sequence[str] | None = None,
    ) -> PaginatedResponseOfDomainResponse:
        data = self._http.get("/domains", params=_list_params(limit, offset, name, channel_ids))
        return PaginatedResponseOfDomainResponse.model_validate(data)

    def retrieve(self, id: str) -> DomainWithDnsResponse:
        data = self._http.get(f"/domains/{id}")
        return DomainWithDnsResponse.model_validate(data)

    def update(
        self,
        id: str,
        *,
        channel_ids: Sequence[str] | None = None,
    ) -> DomainResponse:
        data = self._http.patch(f"/domains/{id}", json=build_body(channel_ids=channel_ids))
        return DomainResponse.model_validate(data)

    def delete(self, id: str) -> None:
        self._http.delete(f"/domains/{id}")

    def verify(self, id: str) -> DnsRecordsResponse:
        data = self._http.post(f"/domains/{id}/verify")
        return DnsRecordsResponse.model_validate(data)

    def rotate_key(self, id: str) -> DnsRecordResponse:
        data = self._http.post(f"/domains/{id}/rotate-key")
        return DnsRecordResponse.model_validate(data)


class AsyncDomainsResource(AsyncBaseResource):
    async def create(
        self,
        *,
        name: str,
        channel_ids: Sequence[str] | None = None,
    ) -> DomainWithDnsResponse:
        body = build_body(name=name, channel_ids=channel_ids)
        data = await self._http.post("/domains", json=body)
        return DomainWithDnsResponse.model_validate(data)

    async def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        name: str | None = None,
        channel_ids: Sequence[str] | None = None,
    ) -> PaginatedResponseOfDomainResponse:
        params = _list_params(limit, offset, name, channel_ids)
        data = await self._http.get("/domains", params=params)
        return PaginatedResponseOfDomainResponse.model_validate(data)

    async def retrieve(self, id: str) -> DomainWithDnsResponse:
        data = await self._http.get(f"/domains/{id}")
        return DomainWithDnsResponse.model_validate(data)

    async def update(
        self,
        id: str,
        *,
        channel_ids: Sequence[str] | None = None,
    ) -> DomainResponse:
        data = await self._http.patch(f"/domains/{id}", json=build_body(channel_ids=channel_ids))
        return DomainResponse.model_validate(data)

    async def delete(self, id: str) -> None:
        await self._http.delete(f"/domains/{id}")

    async def verify(self, id: str) -> DnsRecordsResponse:
        data = await self._http.post(f"/domains/{id}/verify")
        return DnsRecordsResponse.model_validate(data)

    async def rotate_key(self, id: str) -> DnsRecordResponse:
        data = await self._http.post(f"/domains/{id}/rotate-key")
        return DnsRecordResponse.model_validate(data)
