"""Reusable validation helpers."""
from .exceptions import ValidationError


def required_text(value: str, field_name: str) -> str:
    """Return trimmed text or raise a validation error."""
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field_name} is required.")
    return value.strip()


def positive_int(value: int, field_name: str) -> int:
    """Validate a positive integer."""
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValidationError(f"{field_name} must be a positive integer.")
    return value
