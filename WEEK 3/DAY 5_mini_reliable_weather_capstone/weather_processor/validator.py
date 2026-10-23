"""Validation rules for weather records."""
from typing import Any

class DataValidationError(ValueError):
    """Raised when incoming weather data does not match the contract."""


def validate_weather_records(data: Any) -> list[dict[str, Any]]:
    """Validate a non-empty list of records with city and numeric temperature."""
    if not isinstance(data, list):
        raise DataValidationError("Weather data must be a JSON list.")
    records = []
    seen = set()
    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise DataValidationError(f"Record {index} must be a JSON object.")
        city = item.get("city")
        temperature = item.get("temperature")
        if not isinstance(city, str) or not city.strip():
            raise DataValidationError(f"Record {index} has a missing or invalid city.")
        if isinstance(temperature, bool) or not isinstance(temperature, (int, float)):
            raise DataValidationError(f"Record {index} has a non-numeric temperature.")
        if not (-100 <= float(temperature) <= 70):
            raise DataValidationError(f"Record {index} temperature is outside -100..70 C.")
        key = city.strip().casefold()
        if key in seen:
            raise DataValidationError(f"Duplicate city record: {city.strip()}.")
        seen.add(key)
        records.append({"city": city.strip(), "temperature": float(temperature)})
    if not records:
        raise DataValidationError("Weather data must contain at least one record.")
    return records
