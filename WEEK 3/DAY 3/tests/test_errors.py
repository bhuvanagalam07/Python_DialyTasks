"""Error statuses that must fail fast, and the exception hierarchy."""
import pytest
import responses

from weather_client import ApiError, ApiStatusError, MalformedResponseError
from tests.helpers import CUR, HIS, make_client, obs


@responses.activate
@pytest.mark.parametrize("status", [400, 401, 403, 404, 422, 500])
def test_permanent_status_not_retried(status):
    sleeps = []
    responses.get(CUR, status=status)
    with pytest.raises(ApiStatusError) as exc:
        make_client(sleeps).current("London")
    assert exc.value.status_code == status
    assert len(responses.calls) == 1 and sleeps == []


@responses.activate
@pytest.mark.parametrize("body", ["<html>oops</html>", "", "{not json"])
def test_malformed_json_not_retried(body):
    sleeps = []
    responses.get(CUR, body=body, status=200)
    with pytest.raises(MalformedResponseError):
        make_client(sleeps).current("London")
    assert len(responses.calls) == 1 and sleeps == []


@responses.activate
def test_failure_on_second_page_propagates():
    c = make_client([], max_pages=3)
    responses.get(HIS, json={"items": [obs()], "next_page": 2})
    for _ in range(3):
        responses.get(HIS, status=503)
    with pytest.raises(ApiStatusError) as exc:
        c.history("London")
    assert exc.value.status_code == 503 and exc.value.attempts == 3


@responses.activate
def test_all_errors_share_base_class():
    responses.get(CUR, status=404)
    with pytest.raises(ApiError):
        make_client([]).current("London")
