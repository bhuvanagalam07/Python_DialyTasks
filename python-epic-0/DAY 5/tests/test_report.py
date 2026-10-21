import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json

import pytest

from report_generator import ReportGenerator


def create_employee_csv(tmp_path):
    """Create a sample employee CSV file for testing."""
    csv_file = tmp_path / "employees.csv"

    csv_file.write_text(
        "name,department,salary,join_date\n"
        "Arun,IT,45000,2026-08-15\n"
        "Priya,HR,35000,2026-07-20\n"
        "Rahul,IT,55000,2026-05-10\n",
        encoding="utf-8",
    )

    return csv_file


def test_load_employees(tmp_path):
    csv_file = create_employee_csv(tmp_path)

    generator = ReportGenerator(csv_file)
    employees = generator.load_employees()

    assert len(employees) == 3
    assert employees[0]["name"] == "Arun"
    assert employees[0]["department"] == "IT"
    assert employees[0]["salary"] == 45000.0


def test_department_statistics(tmp_path):
    csv_file = create_employee_csv(tmp_path)

    generator = ReportGenerator(csv_file)
    statistics = generator.department_statistics()

    assert statistics["IT"]["employee_count"] == 2
    assert statistics["IT"]["average_salary"] == 50000.0
    assert statistics["HR"]["employee_count"] == 1
    assert statistics["HR"]["average_salary"] == 35000.0


def test_generate_json_report(tmp_path):
    csv_file = create_employee_csv(tmp_path)
    output_file = tmp_path / "employee_report.json"

    generator = ReportGenerator(csv_file)
    report = generator.generate_report(output_file)

    assert report["total_employees"] == 3
    assert output_file.exists()

    saved_report = json.loads(output_file.read_text(encoding="utf-8"))

    assert saved_report["total_employees"] == 3
    assert "department_statistics" in saved_report
    assert "employees_joined_last_90_days" in saved_report


def test_missing_employee_file(tmp_path):
    csv_file = tmp_path / "missing.csv"

    generator = ReportGenerator(csv_file)

    with pytest.raises(FileNotFoundError):
        generator.load_employees()


def test_invalid_csv_headers(tmp_path):
    csv_file = tmp_path / "employees.csv"
    csv_file.write_text(
        "name,age\nArun,25\n",
        encoding="utf-8",
    )

    generator = ReportGenerator(csv_file)

    with pytest.raises(ValueError):
        generator.load_employees()


if __name__ == "__main__":
    import pytest

    sys.exit(pytest.main([__file__, "-v"]))