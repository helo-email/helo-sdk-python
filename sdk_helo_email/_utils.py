from __future__ import annotations

from typing import Any


def to_camel(s: str) -> str:
    """snake_case to camelCase, dropping the underscore keywords get escaped with."""
    if s.endswith("_"):
        s = s[:-1]
    parts = s.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def build_params(**kwargs: Any) -> dict[str, Any] | None:
    """Query parameters with camelCase keys, dropping None values."""
    params = {to_camel(k): v for k, v in kwargs.items() if v is not None}
    return params or None


def build_body(**kwargs: Any) -> dict[str, Any]:
    """Request body with camelCase keys, dropping None values."""
    return {to_camel(k): v for k, v in kwargs.items() if v is not None}


def build_headers(**kwargs: Any) -> dict[str, str] | None:
    """Request headers, dropping None values. Keys are passed through verbatim."""
    headers = {k: v for k, v in kwargs.items() if v is not None}
    return headers or None
