from __future__ import annotations

from collections.abc import Sequence

from .._utils import build_body, build_params
from ..types.domains import (
    DnsRecordResponse,
    DnsRecordsResponse,
    DomainResponse,
    DomainWithDnsResponse,
    PaginatedResponseOfDomainResponse,
)
from ._base import AsyncBaseResource, BaseResource


class DomainsResource(BaseResource):
    def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        name: str | None = None,
        channel_ids: Sequence[str] | None = None,
    ) -> PaginatedResponseOfDomainResponse:
        """List all domains"""

        params = build_params(
            limit=limit,
            offset=offset,
            name=name,
            channel_ids=",".join(channel_ids) if channel_ids else None,
        )
        data = self._http.get("/domains", params=params)
        return PaginatedResponseOfDomainResponse.model_validate(data)

    def create(
        self, *, name: str, channel_ids: Sequence[str] | None = None
    ) -> DomainWithDnsResponse:
        """Create a domain"""

        body = build_body(
            name=name,
            channel_ids=channel_ids if channel_ids else None,
        )
        data = self._http.post("/domains", json=body)
        return DomainWithDnsResponse.model_validate(data)

    def retrieve(self, id: str) -> DomainWithDnsResponse:
        """Retrieve a domain"""

        data = self._http.get(f"/domains/{id}")
        return DomainWithDnsResponse.model_validate(data)

    def update(self, id: str, *, channel_ids: Sequence[str] | None = None) -> DomainResponse:
        """Update a domain"""

        body = build_body(
            channel_ids=channel_ids if channel_ids else None,
        )
        data = self._http.patch(f"/domains/{id}", json=body)
        return DomainResponse.model_validate(data)

    def delete(self, id: str) -> None:
        """Delete a domain"""

        self._http.delete(f"/domains/{id}")

    def verify(self, id: str) -> DnsRecordsResponse:
        """Verify a domain"""

        data = self._http.post(f"/domains/{id}/verify")
        return DnsRecordsResponse.model_validate(data)

    def rotate_key(self, id: str) -> DnsRecordResponse:
        """Rotate a domain key"""

        data = self._http.post(f"/domains/{id}/rotate-key")
        return DnsRecordResponse.model_validate(data)


class AsyncDomainsResource(AsyncBaseResource):
    async def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        name: str | None = None,
        channel_ids: Sequence[str] | None = None,
    ) -> PaginatedResponseOfDomainResponse:
        """List all domains"""

        params = build_params(
            limit=limit,
            offset=offset,
            name=name,
            channel_ids=",".join(channel_ids) if channel_ids else None,
        )
        data = await self._http.get("/domains", params=params)
        return PaginatedResponseOfDomainResponse.model_validate(data)

    async def create(
        self, *, name: str, channel_ids: Sequence[str] | None = None
    ) -> DomainWithDnsResponse:
        """Create a domain"""

        body = build_body(
            name=name,
            channel_ids=channel_ids if channel_ids else None,
        )
        data = await self._http.post("/domains", json=body)
        return DomainWithDnsResponse.model_validate(data)

    async def retrieve(self, id: str) -> DomainWithDnsResponse:
        """Retrieve a domain"""

        data = await self._http.get(f"/domains/{id}")
        return DomainWithDnsResponse.model_validate(data)

    async def update(self, id: str, *, channel_ids: Sequence[str] | None = None) -> DomainResponse:
        """Update a domain"""

        body = build_body(
            channel_ids=channel_ids if channel_ids else None,
        )
        data = await self._http.patch(f"/domains/{id}", json=body)
        return DomainResponse.model_validate(data)

    async def delete(self, id: str) -> None:
        """Delete a domain"""

        await self._http.delete(f"/domains/{id}")

    async def verify(self, id: str) -> DnsRecordsResponse:
        """Verify a domain"""

        data = await self._http.post(f"/domains/{id}/verify")
        return DnsRecordsResponse.model_validate(data)

    async def rotate_key(self, id: str) -> DnsRecordResponse:
        """Rotate a domain key"""

        data = await self._http.post(f"/domains/{id}/rotate-key")
        return DnsRecordResponse.model_validate(data)
