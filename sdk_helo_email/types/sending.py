from __future__ import annotations

from .shared import HeloModel


class SendMessageAcceptedResponse(HeloModel):
    status: str | None = None
    message_id: str | None = None
    suppressions: list[str] | None = None


class SendMessageFailedResponse(HeloModel):
    status: str
    error_code: str
    error_message: str


class SendMessageBatchResponse(HeloModel):
    responses: list[SendMessageAcceptedResponse]


class SendBroadcastResponse(HeloModel):
    status: str | None = None
    broadcast_id: str | None = None
