import csv
import json
from pathlib import Path
import pytest
from weather_processor.report_generator import ReportError, write_reports


def test_writes_json_and_csv(tmp_path):
    summary = {"total_cities": 1, "average_temperature": 22.0, "highest_temperature": 22.0,
               "hottest_city": "Pune", "lowest_temperature": 22.0, "coldest_city": "Pune",
               "records": [{"city": "Pune", "temperature": 22.0}], "data_source": "test"}
    json_path, csv_path = write_reports(summary, tmp_path / "out")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["total_cities"] == 1
    assert "generated_at_utc" in payload
    with csv_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows == [{"city": "Pune", "temperature": "22.0"}]


def test_report_failure_is_recoverable(tmp_path):
    blocked = tmp_path / "a_file"
    blocked.write_text("not a directory", encoding="utf-8")
    with pytest.raises(ReportError, match="Could not write reports"):
        write_reports({"records": []}, blocked / "reports")
