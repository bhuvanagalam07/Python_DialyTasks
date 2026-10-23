import pytest
import requests

from src.weather_client import WeatherAPIError, WeatherClient
from tests.conftest import FakeResponse, FakeSession


def test_successful_weather_request(client, successful_session):
    result = client.get_weather("Hyderabad", session=successful_session)

    assert result["city"] == "Hyderabad"
    assert result["temperature"] == 30

    url, kwargs = successful_session.calls[0]
    assert url == "https://weather.example.test/weather"
    assert kwargs["params"] == {"city": "Hyderabad"}
    assert kwargs["timeout"] == 3


@pytest.mark.parametrize("city", ["", "   ", None, 123])
def test_invalid_city_is_rejected(client, city):
    with pytest.raises(ValueError, match="city must not be empty"):
        client.get_weather(city)


@pytest.mark.parametrize("timeout", [0, -1, -5])
def test_invalid_timeout_is_rejected(timeout):
    with pytest.raises(ValueError, match="positive number"):
        WeatherClient("https://weather.example.test", timeout=timeout)


@pytest.mark.parametrize("base_url", ["", "   ", None])
def test_invalid_base_url_is_rejected(base_url):
    with pytest.raises(ValueError, match="base_url"):
        WeatherClient(base_url)


def test_timeout_is_handled(client):
    session = FakeSession(error=requests.Timeout("connection timed out"))

    with pytest.raises(WeatherAPIError, match="timed out"):
        client.get_weather("Hyderabad", session=session)


def test_http_error_is_handled(client):
    session = FakeSession(
        response=FakeResponse(
            status_error=requests.HTTPError("503 Service Unavailable")
        )
    )

    with pytest.raises(WeatherAPIError, match="request failed"):
        client.get_weather("Hyderabad", session=session)


def test_malformed_json_is_handled(client):
    session = FakeSession(
        response=FakeResponse(json_error=ValueError("invalid JSON"))
    )

    with pytest.raises(WeatherAPIError, match="invalid JSON"):
        client.get_weather("Hyderabad", session=session)


@pytest.mark.parametrize("data", [None, [], "invalid", 123])
def test_non_object_response_is_rejected(client, data):
    session = FakeSession(response=FakeResponse(data=data))

    with pytest.raises(WeatherAPIError, match="JSON object"):
        client.get_weather("Hyderabad", session=session)


def test_missing_temperature_is_rejected(client):
    session = FakeSession(
        response=FakeResponse(data={"city": "Hyderabad"})
    )

    with pytest.raises(WeatherAPIError, match="missing temperature"):
        client.get_weather("Hyderabad", session=session)


def test_city_whitespace_is_trimmed(client, successful_session):
    client.get_weather("  Hyderabad  ", session=successful_session)

    _, kwargs = successful_session.calls[0]
    assert kwargs["params"]["city"] == "Hyderabad"
