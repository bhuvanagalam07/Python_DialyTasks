import pytest

from src.weather_client import WeatherClient


class FakeResponse:
    def __init__(self, data=None, status_error=None, json_error=None):
        self.data = data
        self.status_error = status_error
        self.json_error = json_error

    def raise_for_status(self):
        if self.status_error:
            raise self.status_error

    def json(self):
        if self.json_error:
            raise self.json_error
        return self.data


class FakeSession:
    def __init__(self, response=None, error=None):
        self.response = response
        self.error = error
        self.calls = []

    def get(self, url, **kwargs):
        self.calls.append((url, kwargs))
        if self.error:
            raise self.error
        return self.response


@pytest.fixture
def client():
    return WeatherClient(
        base_url="https://weather.example.test",
        timeout=3,
    )


@pytest.fixture
def successful_session():
    return FakeSession(
        response=FakeResponse(
            data={"city": "Hyderabad", "temperature": 30}
        )
    )
