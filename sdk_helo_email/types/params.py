"""TypedDicts for the object-shaped values accepted by request bodies.

They give editor completion and static checking for arguments that would
otherwise be bare dicts, and are plain ``dict`` subclasses at runtime, so passing
a literal dict keeps working.

Keys use the API's own casing (``fileName``), because nested objects are
forwarded to the API verbatim — unlike the snake_case keyword arguments on
resource methods, which are converted for you.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from typing_extensions import NotRequired, TypedDict

from .shared import AttachmentDisposition


class CreateChannelTrackingParam(TypedDict, total=False):
    links: bool
    opens: bool


class UpdateChannelTrackingParam(TypedDict, total=False):
    links: bool
    opens: bool


class MailAddressParam(TypedDict):
    email: str
    name: NotRequired[str]


class SendMessageRequestTemplateParam(TypedDict, total=False):
    subject: str
    html: str
    text: str
    inlineStyles: bool
    data: dict[str, Any]


class SendMessageRequestTrackingParam(TypedDict, total=False):
    opens: bool
    links: bool


class AttachmentParam(TypedDict):
    content: str
    contentId: NotRequired[str]
    contentType: NotRequired[str]
    fileName: str
    disposition: AttachmentDisposition


# `SendMessageRequest` has a key that is a Python keyword, so it needs the
# functional TypedDict form.
SendMessageRequestParam = TypedDict(
    "SendMessageRequestParam",
    {
        "from": MailAddressParam,
        "to": Sequence[MailAddressParam],
        "cc": NotRequired[Sequence[MailAddressParam]],
        "bcc": NotRequired[Sequence[MailAddressParam]],
        "replyTo": NotRequired[Sequence[MailAddressParam]],
        "subject": NotRequired[str],
        "html": NotRequired[str],
        "text": NotRequired[str],
        "template": NotRequired[SendMessageRequestTemplateParam],
        "tracking": NotRequired[SendMessageRequestTrackingParam],
        "attachments": NotRequired[Sequence[AttachmentParam]],
        "tags": NotRequired[Sequence[str]],
        "headers": NotRequired[dict[str, str]],
        "metadata": NotRequired[dict[str, str]],
    },
)


class SendBroadcastRequestTemplateParam(TypedDict):
    subject: str
    html: NotRequired[str]
    text: NotRequired[str]
    inlineStyles: NotRequired[bool]
    data: NotRequired[dict[str, Any]]


class SendBroadcastRequestTrackingParam(TypedDict, total=False):
    opens: bool
    links: bool


class SendBroadcastRequestMessageParam(TypedDict):
    to: Sequence[MailAddressParam]
    cc: NotRequired[Sequence[MailAddressParam]]
    bcc: NotRequired[Sequence[MailAddressParam]]
    tags: NotRequired[Sequence[str]]
    headers: NotRequired[dict[str, str]]
    metadata: NotRequired[dict[str, str]]
    data: NotRequired[dict[str, Any]]


class WebhookHeaderParam(TypedDict):
    name: str
    value: str
