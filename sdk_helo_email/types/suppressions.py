from __future__ import annotations

from datetime import datetime

from .shared import HeloModel, MailType, SuppressionReason


class SuppressionResponse(HeloModel):
    email: str
    reason: SuppressionReason
    created_at: datetime


class PaginatedResponseOfSuppressionResponse(HeloModel):
    total_count: int
    results: list[SuppressionResponse]


class CreateSuppressionsRequest(HeloModel):
    channel_id: str
    mail_type: MailType
    emails: list[str]


class SuppressionResult(HeloModel):
    email: str
    success: bool
    message: str | None = None


class CreateSuppressionsResponse(HeloModel):
    results: list[SuppressionResult]


class RemoveSuppressionsRequest(HeloModel):
    channel_id: str
    mail_type: MailType
    emails: list[str]


class RemoveSuppressionResult(HeloModel):
    email: str
    success: bool
    message: str | None = None


class RemoveSuppressionsResponse(HeloModel):
    results: list[RemoveSuppressionResult]
