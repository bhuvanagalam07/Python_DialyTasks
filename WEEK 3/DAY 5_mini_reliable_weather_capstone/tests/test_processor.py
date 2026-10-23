import pytest
from weather_processor.processor import process_weather_data
from weather_processor.validator import DataValidationError


def test_summary_calculates_expected_values():
    result = process_weather_data([
        {"city": "Hyderabad", "temperature": 32},
        {"city": "Visakhapatnam", "temperature": 29},
        {"city": "Bengaluru", "temperature": 25},
    ])
    assert result["total_cities"] == 3
    assert result["average_temperature"] == 28.67
    assert result["hottest_city"] == "Hyderabad"
    assert result["coldest_city"] == "Bengaluru"


def test_invalid_input_fails_before_processing():
    with pytest.raises(DataValidationError):
        process_weather_data([{"city": "X", "temperature": "warm"}])
