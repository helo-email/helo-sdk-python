"""TypedDicts for request parameters.

These give editor completion and static checking for the dict-shaped arguments
accepted by the resource methods. They are plain ``dict`` subclasses at runtime,
so existing callers passing literal dicts keep working.

Note: nested objects are sent to the API verbatim, so their keys use the API's
casing (e.g. ``fileName``), unlike the snake_case keyword arguments on resource
methods which are converted automatically.
"""

from __future__ import annotations

from typing import Any

from typing_extensions import NotRequired, TypedDict


class MailAddressParam(TypedDict):
    email: str
    name: NotRequired[str]


class TrackingParam(TypedDict, total=False):
    links: bool
    opens: bool


class AttachmentParam(TypedDict):
    content: str
    fileName: str
    disposition: str
    contentType: NotRequired[str]
    contentId: NotRequired[str]


class WebhookHeaderParam(TypedDict):
    name: str
    value: str


# Free-form objects forwarded to the API as-is.
TemplateParam = dict[str, Any]
MetadataParam = dict[str, Any]
HeadersParam = dict[str, str]
