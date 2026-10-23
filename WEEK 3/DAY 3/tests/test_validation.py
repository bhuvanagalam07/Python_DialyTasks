"""Payload validation (unit level + through the client)."""
import pytest
import responses

from weather_client import MalformedResponseError
from weather_client.validators import validate_observation, validate_page
from tests.helpers import CUR, HIS, make_client, obs

BAD_OBSERVATIONS = [
    {"city": "London"},          # missing fields
    obs(temp="hot"),             # wrong type
    obs(temp=True),              # bool is not a temperature
    obs(temp=900),               # out of range
    obs(temp=-101),              # out of range (low)
    obs(condition=""),           # empty string
    ["not", "an", "object"],     # wrong top-level type
    None,
]


@pytest.mark.parametrize("payload", BAD_OBSERVATIONS)
def test_bad_observation_rejected(payload):
    with pytest.raises(MalformedResponseError):
        validate_observation(payload)


@pytest.mark.parametrize("temp", [-100, 70, 0, 14.5])
def test_temperature_boundaries_accepted(temp):
    assert validate_observation(obs(temp=temp)).temperature_c == float(temp)


@pytest.mark.parametrize("bad_next", [1, 0, "2", 2.5, True])
def test_non_advancing_next_page_rejected(bad_next):
    with pytest.raises(MalformedResponseError):
        validate_page({"items": [], "next_page": bad_next}, current_page=1)


@pytest.mark.parametrize("payload", [{"next_page": None}, {"items": "x"}, [], None])
def test_bad_page_envelope_rejected(payload):
    with pytest.raises(MalformedResponseError):
        validate_page(payload, current_page=1)


@responses.activate
def test_client_rejects_bad_current_payload():
    responses.get(CUR, json={"city": "London"})
    with pytest.raises(MalformedResponseError):
        make_client([]).current("London")


@responses.activate
def test_client_does_not_loop_on_bad_cursor():
    responses.get(HIS, json={"items": [obs()], "next_page": 1})
    with pytest.raises(MalformedResponseError):
        make_client([]).history("London")
    assert len(responses.calls) == 1
