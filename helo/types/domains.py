from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from .shared import DeliveryType, DnsRecordStatus, DnsRecordType, HeloModel


class DomainChannelResponse(HeloModel):
    id: str
    name: str
    delivery_type: DeliveryType
    deleted: Optional[bool] = None


class DnsRecordResponse(HeloModel):
    type: Optional[DnsRecordType] = None
    host: Optional[str] = None
    value: Optional[str] = None
    status: Optional[DnsRecordStatus] = None


class DnsRecordsResponse(HeloModel):
    domain_key_active: Optional[DnsRecordResponse] = None
    domain_key_pending: Optional[DnsRecordResponse] = None
    return_path: Optional[List[DnsRecordResponse]] = None
    tracking: Optional[DnsRecordResponse] = None
    unsubscribe: Optional[DnsRecordResponse] = None


class DomainResponse(HeloModel):
    id: str
    created_at: datetime
    name: str
    verified: bool
    channels: Optional[List[DomainChannelResponse]] = None


class DomainWithDnsResponse(HeloModel):
    id: str
    created_at: datetime
    name: str
    verified: bool
    channels: Optional[List[DomainChannelResponse]] = None
    dns_records: DnsRecordsResponse


class PaginatedResponseOfDomainResponse(HeloModel):
    total_count: int
    results: List[DomainResponse]
