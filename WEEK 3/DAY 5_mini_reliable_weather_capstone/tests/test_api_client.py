import requests
import pytest
from unittest.mock import Mock
from weather_processor.api_client import ApiClientError, WeatherApiClient


def response(payload, status=200):
    r = Mock()
    r.status_code = status
    r.json.return_value = payload
    r.raise_for_status.return_value = None
    return r


def test_api_success_uses_timeout_and_returns_record():
    session = Mock()
    session.get.return_value = response({"current": {"temperature_2m": 26.5}})
    client = WeatherApiClient(timeout=3, max_retries=0, session=session)
    assert client.get_current_weather("Pune", 18.52, 73.85) == {"city": "Pune", "temperature": 26.5}
    assert session.get.call_args.kwargs["timeout"] == 3


def test_timeout_retries_then_returns_controlled_error():
    session = Mock()
    session.get.side_effect = requests.Timeout("slow")
    client = WeatherApiClient(timeout=0.01, max_retries=1, session=session)
    with pytest.raises(ApiClientError, match="after 2 attempt"):
        client.get_current_weather("Pune", 18.52, 73.85)
    assert session.get.call_count == 2


def test_malformed_api_response_is_rejected():
    session = Mock()
    session.get.return_value = response({"unexpected": {}})
    client = WeatherApiClient(max_retries=0, session=session)
    with pytest.raises(ApiClientError, match="malformed response"):
        client.get_current_weather("Pune", 18.52, 73.85)


def test_http_500_retries_once():
    session = Mock()
    bad = Mock()
    bad.status_code = 500
    bad.raise_for_status.side_effect = requests.HTTPError(response=bad)
    session.get.side_effect = [bad, response({"current": {"temperature_2m": 24}})]
    client = WeatherApiClient(max_retries=1, session=session)
    assert client.get_current_weather("Pune", 18.52, 73.85)["temperature"] == 24
    assert session.get.call_count == 2
