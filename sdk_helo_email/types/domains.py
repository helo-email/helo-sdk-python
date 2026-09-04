from __future__ import annotations

from datetime import datetime

from pydantic import Field

from .shared import DeliveryType, DnsRecordStatus, DnsRecordType, HeloModel


class CreateDomainRequest(HeloModel):
    name: str
    channel_ids: list[str] | None = None


class DnsRecordResponse(HeloModel):
    type_: DnsRecordType | None = Field(default=None, alias="type")
    host: str | None = None
    value: str | None = None
    status: DnsRecordStatus | None = None
    last_checked_at: datetime | None = None


class DnsRecordsResponse(HeloModel):
    domain_key_active: DnsRecordResponse | None = None
    domain_key_pending: DnsRecordResponse | None = None
    return_path: list[DnsRecordResponse] | None = None


class DomainChannelResponse(HeloModel):
    id: str
    name: str
    delivery_type: DeliveryType
    deleted: bool | None = None


class DomainResponse(HeloModel):
    id: str
    created_at: datetime
    name: str
    verified: bool
    channels: list[DomainChannelResponse] | None = None


class DomainWithDnsResponse(HeloModel):
    id: str
    created_at: datetime
    name: str
    verified: bool
    channels: list[DomainChannelResponse] | None = None
    dns_records: DnsRecordsResponse


class PaginatedResponseOfDomainResponse(HeloModel):
    total_count: int
    results: list[DomainResponse]


class UpdateDomainRequest(HeloModel):
    channel_ids: list[str] | None = None
