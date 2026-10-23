"""Collection processing and business rules."""
from statistics import mean
from typing import Any
from .validator import validate_weather_records


def process_weather_data(data: Any) -> dict[str, Any]:
    records = validate_weather_records(data)
    temperatures = [record["temperature"] for record in records]
    hottest = max(records, key=lambda record: record["temperature"])
    coldest = min(records, key=lambda record: record["temperature"])
    return {
        "total_cities": len(records),
        "average_temperature": round(mean(temperatures), 2),
        "highest_temperature": hottest["temperature"],
        "hottest_city": hottest["city"],
        "lowest_temperature": coldest["temperature"],
        "coldest_city": coldest["city"],
        "records": records,
    }
