from __future__ import annotations

from typing import Any, Dict, List, Optional

from .._utils import build_body
from ..types.domains import (
    DnsRecordResponse,
    DnsRecordsResponse,
    DomainResponse,
    DomainWithDnsResponse,
    PaginatedResponseOfDomainResponse,
)
from ._base import BaseResource


class DomainsResource(BaseResource):
    def create(
        self,
        *,
        name: str,
        channel_ids: Optional[List[str]] = None,
    ) -> DomainWithDnsResponse:
        body = build_body(name=name, channel_ids=channel_ids)
        data = self._http.post("/domains", json=body)
        return DomainWithDnsResponse.model_validate(data)

    def list(
        self,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        name: Optional[str] = None,
        channel_ids: Optional[List[str]] = None,
    ) -> PaginatedResponseOfDomainResponse:
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if name is not None:
            params["name"] = name
        if channel_ids is not None:
            params["channelIds"] = ",".join(channel_ids)
        data = self._http.get("/domains", params=params or None)
        return PaginatedResponseOfDomainResponse.model_validate(data)

    def retrieve(self, id: str) -> DomainWithDnsResponse:
        data = self._http.get(f"/domains/{id}")
        return DomainWithDnsResponse.model_validate(data)

    def update(
        self,
        id: str,
        *,
        channel_ids: Optional[List[str]] = None,
    ) -> DomainResponse:
        body = build_body(channel_ids=channel_ids)
        data = self._http.patch(f"/domains/{id}", json=body)
        return DomainResponse.model_validate(data)

    def delete(self, id: str) -> None:
        self._http.delete(f"/domains/{id}")

    def verify(self, id: str) -> DnsRecordsResponse:
        data = self._http.post(f"/domains/{id}/verify")
        return DnsRecordsResponse.model_validate(data)

    def rotate_key(self, id: str) -> DnsRecordResponse:
        data = self._http.post(f"/domains/{id}/rotate-key")
        return DnsRecordResponse.model_validate(data)
