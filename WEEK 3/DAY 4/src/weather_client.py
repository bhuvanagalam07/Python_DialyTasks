import requests


class WeatherClientError(Exception):
    """Base exception for weather client errors."""


class WeatherAPIError(WeatherClientError):
    """Raised when the API returns an error or invalid response."""


class WeatherClient:
    def __init__(self, base_url, timeout=5):
        if not isinstance(base_url, str) or not base_url.strip():
            raise ValueError("base_url must not be empty")

        if (
            not isinstance(timeout, (int, float))
            or isinstance(timeout, bool)
            or timeout <= 0
        ):
            raise ValueError("timeout must be a positive number")

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get_weather(self, city, session=None):
        if not isinstance(city, str) or not city.strip():
            raise ValueError("city must not be empty")

        http = session if session is not None else requests

        try:
            response = http.get(
                f"{self.base_url}/weather",
                params={"city": city.strip()},
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
        except requests.Timeout as exc:
            raise WeatherAPIError("Weather request timed out") from exc
        except requests.RequestException as exc:
            raise WeatherAPIError("Weather API request failed") from exc
        except ValueError as exc:
            raise WeatherAPIError("Weather API returned invalid JSON") from exc

        if not isinstance(data, dict):
            raise WeatherAPIError("Weather API response must be a JSON object")

        if "temperature" not in data:
            raise WeatherAPIError("Weather response is missing temperature")

        return data
