from __future__ import annotations

from typing import Any


def to_camel(s: str) -> str:
    if s.endswith("_"):
        s = s[:-1]
    parts = s.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def build_params(**kwargs: Any) -> dict[str, Any]:
    """Convert snake_case kwargs to camelCase, dropping None values."""
    return {to_camel(k): v for k, v in kwargs.items() if v is not None}


def build_body(**kwargs: Any) -> dict[str, Any]:
    """Build a request body dict with camelCase keys, dropping None values."""
    result: dict[str, Any] = {}
    for k, v in kwargs.items():
        if v is not None:
            camel_k = to_camel(k)
            result[camel_k] = v
    return result
