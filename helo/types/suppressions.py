from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from .shared import HeloModel, SuppressionReason


class SuppressionResponse(HeloModel):
    email: str
    reason: SuppressionReason
    created_at: datetime


class PaginatedResponseOfSuppressionResponse(HeloModel):
    total_count: int
    results: List[SuppressionResponse]


class SuppressionResult(HeloModel):
    email: str
    success: bool
    message: Optional[str] = None


class CreateSuppressionsResponse(HeloModel):
    results: List[SuppressionResult]


class RemoveSuppressionResult(HeloModel):
    email: str
    success: bool
    message: Optional[str] = None


class RemoveSuppressionsResponse(HeloModel):
    results: List[RemoveSuppressionResult]
