import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
from datetime import datetime
from unittest.mock import Mock, patch

import requests

from api_monitor import ApiMonitor
from models import ApiResult


def test_successful_api_check():
    monitor = ApiMonitor(max_retries=1)

    mock_response = Mock()
    mock_response.status_code = 200

    with patch("api_monitor.requests.get", return_value=mock_response):
        result = monitor.check_url("https://example.com")

    assert result.success is True
    assert result.status_code == 200
    assert result.url == "https://example.com"


def test_failed_api_check():
    monitor = ApiMonitor(max_retries=1)

    mock_response = Mock()
    mock_response.status_code = 404

    with patch("api_monitor.requests.get", return_value=mock_response):
        result = monitor.check_url("https://example.com/missing")

    assert result.success is False
    assert result.status_code == 404


def test_timeout_api_check():
    monitor = ApiMonitor(max_retries=1)

    with patch(
        "api_monitor.requests.get",
        side_effect=requests.exceptions.Timeout,
    ):
        result = monitor.check_url("https://example.com")

    assert result.success is False
    assert result.status_code is None


def test_load_urls(tmp_path):
    urls_file = tmp_path / "urls.txt"
    urls_file.write_text(
        "# Sample URLs\nhttps://example.com\n\nhttps://example.org\n",
        encoding="utf-8",
    )

    monitor = ApiMonitor()
    urls = monitor.load_urls(urls_file)

    assert urls == [
        "https://example.com",
        "https://example.org",
    ]


def test_missing_urls_file(tmp_path):
    monitor = ApiMonitor()

    with patch("api_monitor.requests.get") as mock_get:
        import pytest

        with pytest.raises(FileNotFoundError):
            monitor.load_urls(tmp_path / "missing.txt")

        mock_get.assert_not_called()


def test_save_results(tmp_path):
    monitor = ApiMonitor()
    output_file = tmp_path / "api_data.json"

    result = ApiResult(
        url="https://example.com",
        status_code=200,
        response_time=0.25,
        success=True,
        checked_at=datetime(2026, 10, 9, 10, 0, 0),
    )

    monitor.save_results([result], output_file)

    assert output_file.exists()

    data = json.loads(output_file.read_text(encoding="utf-8"))

    assert len(data) == 1
    assert data[0]["url"] == "https://example.com"
    assert data[0]["status_code"] == 200
    assert data[0]["success"] is True

if __name__ == "__main__":
    import pytest

    sys.exit(pytest.main([__file__, "-v"]))
