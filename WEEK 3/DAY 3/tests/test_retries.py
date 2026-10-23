"""Timeouts and safe transient retries."""
import pytest
import requests
import responses

from weather_client import (ApiConnectionError, ApiStatusError, ApiTimeoutError, RetryPolicy)
from tests.helpers import CUR, make_client, obs


@responses.activate
def test_timeout_then_success():
    sleeps = []
    responses.get(CUR, body=requests.exceptions.ReadTimeout("slow"))
    responses.get(CUR, json=obs())
    assert make_client(sleeps).current("London").city == "London"
    assert len(responses.calls) == 2 and sleeps == [0.5]


@responses.activate
def test_timeout_exhausted():
    sleeps = []
    for _ in range(3):
        responses.get(CUR, body=requests.exceptions.ConnectTimeout("nope"))
    with pytest.raises(ApiTimeoutError):
        make_client(sleeps).current("London")
    assert len(responses.calls) == 3 and sleeps == [0.5, 1.0]  # no sleep after last attempt


@responses.activate
def test_connection_error_retried_then_raised():
    for _ in range(3):
        responses.get(CUR, body=requests.exceptions.ConnectionError("refused"))
    with pytest.raises(ApiConnectionError):
        make_client([]).current("London")
    assert len(responses.calls) == 3


@responses.activate
@pytest.mark.parametrize("status", [429, 502, 503, 504])
def test_transient_status_then_success(status):
    responses.get(CUR, status=status)
    responses.get(CUR, json=obs())
    assert make_client([]).current("London").city == "London"
    assert len(responses.calls) == 2


@responses.activate
def test_transient_status_exhausted():
    for _ in range(3):
        responses.get(CUR, status=503)
    with pytest.raises(ApiStatusError) as exc:
        make_client([]).current("London")
    assert exc.value.status_code == 503 and exc.value.attempts == 3


@responses.activate
def test_retry_after_honoured():
    sleeps = []
    responses.get(CUR, status=429, headers={"Retry-After": "1"})
    responses.get(CUR, json=obs())
    make_client(sleeps).current("London")
    assert sleeps == [1.0]


@responses.activate
def test_retry_after_capped():
    sleeps = []
    responses.get(CUR, status=429, headers={"Retry-After": "999"})
    responses.get(CUR, json=obs())
    make_client(sleeps).current("London")
    assert sleeps == [2.0]


@responses.activate
def test_backoff_doubles_and_is_capped():
    sleeps = []
    for _ in range(5):
        responses.get(CUR, status=503)
    with pytest.raises(ApiStatusError):
        make_client(sleeps, max_attempts=5).current("London")
    assert sleeps == [0.5, 1.0, 2.0, 2.0]


@responses.activate
def test_single_attempt_never_retries():
    sleeps = []
    responses.get(CUR, status=503)
    with pytest.raises(ApiStatusError):
        make_client(sleeps, max_attempts=1).current("London")
    assert len(responses.calls) == 1 and sleeps == []


def test_invalid_policy_rejected():
    with pytest.raises(ValueError):
        RetryPolicy(max_attempts=0)
