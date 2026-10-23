import pytest
from weather_processor.validator import DataValidationError, validate_weather_records


def test_valid_records_are_normalized():
    result = validate_weather_records([{"city": " Hyderabad ", "temperature": 30}])
    assert result == [{"city": "Hyderabad", "temperature": 30.0}]

@pytest.mark.parametrize("data", [None, {}, "bad", []])
def test_invalid_top_level_or_empty_data(data):
    with pytest.raises(DataValidationError):
        validate_weather_records(data)

@pytest.mark.parametrize("record", [
    {"city": "", "temperature": 20},
    {"city": "X", "temperature": "hot"},
    {"city": "X", "temperature": True},
    {"city": "X", "temperature": 100},
])
def test_invalid_record_is_rejected(record):
    with pytest.raises(DataValidationError):
        validate_weather_records([record])

def test_duplicate_city_is_rejected_case_insensitively():
    with pytest.raises(DataValidationError, match="Duplicate city"):
        validate_weather_records([{"city": "Pune", "temperature": 20}, {"city": "pune", "temperature": 21}])
