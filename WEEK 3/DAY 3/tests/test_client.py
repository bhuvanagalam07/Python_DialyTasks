"""Happy paths and pagination bounds."""
import pytest
import responses

from weather_client import PaginationLimitError
from tests.helpers import CUR, HIS, BASE, make_client, obs


@pytest.fixture
def client():
    return make_client([], max_pages=3, max_items=10, page_size=2)


@responses.activate
def test_current_success(client):
    responses.get(CUR, json=obs())
    o = client.current("London")
    assert (o.city, o.temperature_c, o.condition) == ("London", 14.5, "Cloudy")


@responses.activate
def test_city_is_url_encoded(client):
    responses.get(f"{BASE}/v1/locations/San%20Francisco/current", json=obs(city="San Francisco"))
    assert client.current("San Francisco").city == "San Francisco"


@pytest.mark.parametrize("city", ["", "   "])
def test_blank_city_rejected(client, city):
    with pytest.raises(ValueError):
        client.current(city)


@responses.activate
def test_history_follows_pages(client):
    responses.get(HIS, json={"items": [obs(1), obs(2)], "next_page": 2})
    responses.get(HIS, json={"items": [obs(3)], "next_page": None})
    assert [o.temperature_c for o in client.history("London")] == [1.0, 2.0, 3.0]
    assert "page=2" in responses.calls[1].request.url


@responses.activate
def test_history_empty(client):
    responses.get(HIS, json={"items": [], "next_page": None})
    assert client.history("London") == []


@responses.activate
def test_exactly_max_pages_allowed(client):
    responses.get(HIS, json={"items": [obs(1)], "next_page": 2})
    responses.get(HIS, json={"items": [obs(2)], "next_page": 3})
    responses.get(HIS, json={"items": [obs(3)], "next_page": None})
    assert len(client.history("London")) == 3


@responses.activate
def test_stops_at_max_pages_boundary(client):
    for n in (1, 2, 3):
        responses.get(HIS, json={"items": [obs(n)], "next_page": n + 1})
    with pytest.raises(PaginationLimitError):
        client.history("London")
    assert len(responses.calls) == 3  # 4th page never requested


@responses.activate
def test_stops_at_max_items():
    c = make_client([], max_pages=10, max_items=3, page_size=2)
    responses.get(HIS, json={"items": [obs(1), obs(2)], "next_page": 2})
    responses.get(HIS, json={"items": [obs(3), obs(4)], "next_page": 3})
    with pytest.raises(PaginationLimitError):
        c.history("London")
    assert len(responses.calls) == 2


def test_invalid_limits_rejected():
    with pytest.raises(ValueError):
        make_client([], max_pages=0)
