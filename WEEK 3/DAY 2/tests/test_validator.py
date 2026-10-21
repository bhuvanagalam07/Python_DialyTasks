import pytest

from validator import validate_weather


def valid_weather():
    return {"city": "Visakhapatnam", "temperature": 30, "humidity": 65}


def test_valid_weather_record():
    data = valid_weather()
    assert validate_weather(data) == data


def test_missing_humidity_is_rejected():
    data = {"city": "Visakhapatnam", "temperature": 30}
    with pytest.raises(ValueError, match="humidity"):
        validate_weather(data)


def test_temperature_string_is_rejected():
    data = {"city": "Visakhapatnam", "temperature": "hot", "humidity": 65}
    with pytest.raises(ValueError, match="Temperature must be numeric"):
        validate_weather(data)


def test_humidity_out_of_range_is_rejected():
    data = {"city": "Visakhapatnam", "temperature": 30, "humidity": 120}
    with pytest.raises(ValueError, match="between 0 and 100"):
        validate_weather(data)


def test_empty_city_is_rejected():
    data = {"city": " ", "temperature": 30, "humidity": 65}
    with pytest.raises(ValueError, match="non-empty string"):
        validate_weather(data)


def test_boolean_temperature_is_rejected():
    data = {"city": "Visakhapatnam", "temperature": True, "humidity": 65}
    with pytest.raises(ValueError, match="Temperature must be numeric"):
        validate_weather(data)
