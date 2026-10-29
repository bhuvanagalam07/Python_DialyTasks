import csv
import json
from pathlib import Path

import pytest

from employee_app.models import Employee, ProcessingResult
from employee_app.processor import EmployeeProcessor, validate_employee
from employee_app.reporting import build_department_summary, write_reports

def test_validate_employee_accepts_valid_row():
    employee = validate_employee({
        "name": "Asha", "department": "IT", "salary": "50000",
        "join_date": "2024-01-15"
    }, 2)
    assert employee.name == "Asha"
    assert employee.salary == 50000
    assert employee.join_date.isoformat() == "2024-01-15"

@pytest.mark.parametrize("row, message", [
    ({"name": "", "department": "IT", "salary": "100", "join_date": "2024-01-01"}, "Name"),
    ({"name": "Asha", "department": "IT", "salary": "abc", "join_date": "2024-01-01"}, "Salary"),
    ({"name": "Asha", "department": "IT", "salary": "-2", "join_date": "2024-01-01"}, "negative"),
    ({"name": "Asha", "department": "IT", "salary": "100", "join_date": "yesterday"}, "YYYY-MM-DD"),
])
def test_validate_employee_rejects_invalid_row(row, message):
    with pytest.raises(ValueError, match=message):
        validate_employee(row, 2)

def test_processor_separates_valid_and_invalid_rows(tmp_path):
    source = tmp_path / "employees.csv"
    source.write_text(
        "name,department,salary,join_date\n"
        "Asha,IT,50000,2024-01-15\n"
        "Bad,Sales,nope,2024-02-01\n",
        encoding="utf-8"
    )
    result = EmployeeProcessor().process_csv(source)
    assert len(result.valid_employees) == 1
    assert len(result.rejected_rows) == 1
    assert "Salary" in result.rejected_rows[0]["reason"]

def test_missing_file_raises_clear_error(tmp_path):
    with pytest.raises(FileNotFoundError, match="Input file not found"):
        EmployeeProcessor().process_csv(tmp_path / "missing.csv")

def test_empty_csv_raises_value_error(tmp_path):
    source = tmp_path / "empty.csv"
    source.write_text("", encoding="utf-8")
    with pytest.raises(ValueError, match="empty"):
        EmployeeProcessor().process_csv(source)

def test_summary_and_reports_are_created(tmp_path):
    result = ProcessingResult(
        valid_employees=[
            Employee("Asha", "IT", 50000, __import__("datetime").date(2024, 1, 1)),
            Employee("Ravi", "IT", 70000, __import__("datetime").date(2024, 2, 1)),
        ],
        rejected_rows=[{"row_number": "4", "reason": "Bad salary", "name": "X",
                        "department": "IT", "salary": "bad", "join_date": "2024-03-01"}],
    )
    summary = build_department_summary(result)
    assert summary == [{"department": "IT", "headcount": 2, "average_salary": 60000.0}]
    paths = write_reports(result, tmp_path / "reports")
    assert all(path.exists() for path in paths)
    payload = json.loads((tmp_path / "reports" / "employee_report.json").read_text(encoding="utf-8"))
    assert payload["total_valid"] == 2
    with (tmp_path / "reports" / "rejected.csv").open(encoding="utf-8") as handle:
        assert len(list(csv.DictReader(handle))) == 1
