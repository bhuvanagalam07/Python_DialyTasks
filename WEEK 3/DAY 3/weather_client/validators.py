"""Validation of API payloads. Raises MalformedResponseError on any problem."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .exceptions import MalformedResponseError

REQUIRED_FIELDS = ("city", "timestamp", "temperature_c", "condition")
MIN_TEMP_C, MAX_TEMP_C = -100.0, 70.0


@dataclass(frozen=True)
class Observation:
    city: str
    timestamp: str
    temperature_c: float
    condition: str


def validate_observation(raw: Any) -> Observation:
    if not isinstance(raw, dict):
        raise MalformedResponseError(f"observation must be an object, got {type(raw).__name__}")
    missing = [k for k in REQUIRED_FIELDS if k not in raw]
    if missing:
        raise MalformedResponseError(f"observation missing fields: {missing}")
    temp = raw["temperature_c"]
    if isinstance(temp, bool) or not isinstance(temp, (int, float)):
        raise MalformedResponseError("temperature_c must be a number")
    if not MIN_TEMP_C <= temp <= MAX_TEMP_C:
        raise MalformedResponseError(f"temperature_c out of range: {temp}")
    for key in ("city", "timestamp", "condition"):
        if not isinstance(raw[key], str) or not raw[key].strip():
            raise MalformedResponseError(f"{key} must be a non-empty string")
    return Observation(raw["city"], raw["timestamp"], float(temp), raw["condition"])


def validate_page(payload: Any, current_page: int) -> tuple[list, int | None]:
    """Page shape: {"items": [...], "next_page": int > current_page | null}."""
    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
        raise MalformedResponseError("page must be an object with an 'items' list")
    nxt = payload.get("next_page")
    if nxt is not None and (isinstance(nxt, bool) or not isinstance(nxt, int) or nxt <= current_page):
        # a cursor that doesn't advance would loop forever
        raise MalformedResponseError(f"next_page must be an int > {current_page}, got {nxt!r}")
    return payload["items"], nxt
