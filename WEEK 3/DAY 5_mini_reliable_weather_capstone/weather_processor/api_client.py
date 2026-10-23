"""Small HTTP adapter for the Open-Meteo current-weather endpoint."""
import logging
import time
from typing import Any
import requests

logger = logging.getLogger(__name__)

class ApiClientError(RuntimeError):
    """A recoverable error communicating with the weather API."""

class WeatherApiClient:
    def __init__(self, timeout: float = 5, max_retries: int = 2, session=None):
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")
        if max_retries < 0:
            raise ValueError("max_retries cannot be negative")
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = session or requests.Session()

    def get_current_weather(self, city: str, latitude: float, longitude: float) -> dict[str, Any]:
        if not city.strip():
            raise ValueError("city cannot be empty")
        url = "https://api.open-meteo.com/v1/forecast"
        params = {"latitude": latitude, "longitude": longitude, "current": "temperature_2m"}
        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.get(url, params=params, timeout=self.timeout)
                response.raise_for_status()
                payload = response.json()
                current = payload.get("current") if isinstance(payload, dict) else None
                temperature = current.get("temperature_2m") if isinstance(current, dict) else None
                if isinstance(temperature, bool) or not isinstance(temperature, (int, float)):
                    raise ApiClientError("Weather API returned a malformed response (missing current.temperature_2m).")
                return {"city": city.strip(), "temperature": float(temperature)}
            except (requests.Timeout, requests.ConnectionError) as exc:
                logger.warning("Transient weather API failure for %s (attempt %s/%s)", city, attempt + 1, self.max_retries + 1)
                if attempt >= self.max_retries:
                    raise ApiClientError(f"Weather API unavailable for {city} after {self.max_retries + 1} attempt(s).") from exc
                time.sleep(min(0.2 * (attempt + 1), 1.0))
            except requests.HTTPError as exc:
                status = getattr(exc.response, "status_code", None)
                if status is not None and status >= 500 and attempt < self.max_retries:
                    time.sleep(min(0.2 * (attempt + 1), 1.0))
                    continue
                raise ApiClientError(f"Weather API returned HTTP error{f' {status}' if status else ''} for {city}.") from exc
            except requests.RequestException as exc:
                raise ApiClientError(f"Weather API request failed for {city}.") from exc
        raise ApiClientError(f"Weather API unavailable for {city}.")
