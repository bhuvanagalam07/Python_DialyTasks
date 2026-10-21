import pytest

from parser import parse_log_line
from exceptions import InvalidLogFormatError


def test_valid_info_log():

    result = parse_log_line(
        "2026-10-06 10:00:00 INFO Application started"
    )

    assert result == (
        "2026-10-06 10:00:00",
        "INFO",
        "Application started"
    )


def test_valid_error_log():

    result = parse_log_line(
        "2026-10-06 10:01:00 ERROR Database failed"
    )

    assert result == (
        "2026-10-06 10:01:00",
        "ERROR",
        "Database failed"
    )


def test_invalid_log_format():

    with pytest.raises(
        InvalidLogFormatError
    ):

        parse_log_line(
            "This is not a valid log"
        )


def test_invalid_log_level():

    with pytest.raises(
        InvalidLogFormatError
    ):

        parse_log_line(
            "2026-10-06 10:00:00 DEBUG Something happened"
        )


def test_empty_log_line():

    with pytest.raises(
        InvalidLogFormatError
    ):

        parse_log_line("")