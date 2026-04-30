from __future__ import annotations

from typing import List, Optional

from .shared import HeloModel


class SendMessageAcceptedResponse(HeloModel):
    status: Optional[str] = None
    message_id: Optional[str] = None
    suppressions: Optional[List[str]] = None


class SendMessageFailedResponse(HeloModel):
    status: str
    error_code: str
    error_message: str


class SendMessageBatchResponse(HeloModel):
    responses: List[SendMessageAcceptedResponse]


class SendBroadcastResponse(HeloModel):
    status: Optional[str] = None
    broadcast_id: Optional[str] = None
