import csv
from pathlib import Path
from datetime import datetime

import pytest

from employee_report import (
    parse_date,
    validate_row,
    department_statistics,
    employees_joined_last_90_days,
    write_rejected_csv,
)


# ---------------------------------------------------------
# Test 1: Valid Date
# ---------------------------------------------------------

def test_parse_valid_date():
    result = parse_date("2026-08-15")

    assert result == datetime(2026, 8, 15)


# ---------------------------------------------------------
# Test 2: Invalid Date
# ---------------------------------------------------------

def test_parse_invalid_date():
    result = parse_date("15-08-2026")

    assert result is None


# ---------------------------------------------------------
# Test 3: Valid Employee Row
# ---------------------------------------------------------

def test_valid_employee_row():

    row = {
        "name": "Rahul Sharma",
        "department": "IT",
        "salary": "65000",
        "join_date": "2026-08-15"
    }

    seen_rows = set()

    is_valid, reason = validate_row(
        row,
        seen_rows
    )

    assert is_valid is True
    assert reason == ""


# ---------------------------------------------------------
# Test 4: Non-Numeric Salary
# ---------------------------------------------------------

def test_non_numeric_salary():

    row = {
        "name": "John Test",
        "department": "IT",
        "salary": "abc",
        "join_date": "2026-08-01"
    }

    seen_rows = set()

    is_valid, reason = validate_row(
        row,
        seen_rows
    )

    assert is_valid is False
    assert reason == "Non-numeric salary"


# ---------------------------------------------------------
# Test 5: Missing Salary
# ---------------------------------------------------------

def test_missing_salary():

    row = {
        "name": "Missing Salary",
        "department": "HR",
        "salary": "",
        "join_date": "2026-08-05"
    }

    seen_rows = set()

    is_valid, reason = validate_row(
        row,
        seen_rows
    )

    assert is_valid is False
    assert reason == "Missing value: salary"


# ---------------------------------------------------------
# Test 6: Duplicate Employee
# ---------------------------------------------------------

def test_duplicate_employee():

    row = {
        "name": "Duplicate Employee",
        "department": "IT",
        "salary": "70000",
        "join_date": "2026-08-10"
    }

    seen_rows = set()

    # First row should be valid
    is_valid, reason = validate_row(
        row,
        seen_rows
    )

    assert is_valid is True

    # Same row again should be rejected
    is_valid, reason = validate_row(
        row,
        seen_rows
    )

    assert is_valid is False
    assert reason == "Duplicate row"


# ---------------------------------------------------------
# Test 7: Department Statistics
# ---------------------------------------------------------

def test_department_statistics():

    employees = [
        {
            "name": "Employee 1",
            "department": "IT",
            "salary": 60000,
            "join_date": "2026-08-01"
        },
        {
            "name": "Employee 2",
            "department": "IT",
            "salary": 80000,
            "join_date": "2026-08-02"
        },
        {
            "name": "Employee 3",
            "department": "HR",
            "salary": 50000,
            "join_date": "2026-08-03"
        }
    ]

    result = department_statistics(employees)

    assert result["IT"]["headcount"] == 2
    assert result["IT"]["average_salary"] == 70000

    assert result["HR"]["headcount"] == 1
    assert result["HR"]["average_salary"] == 50000


# ---------------------------------------------------------
# Test 8: Recent Employees
# ---------------------------------------------------------

def test_employees_joined_last_90_days():

    # Use today's date so this test remains reliable.
    today = datetime.today()

    recent_date = today.strftime("%Y-%m-%d")

    employees = [
        {
            "name": "Recent Employee",
            "department": "IT",
            "salary": 60000,
            "join_date": recent_date
        }
    ]

    result = employees_joined_last_90_days(
        employees
    )

    assert len(result) == 1
    assert result[0]["name"] == "Recent Employee"


# ---------------------------------------------------------
# Test 9: Rejected CSV File
# ---------------------------------------------------------

def test_write_rejected_csv(tmp_path):

    rejected_rows = [
        {
            "row_number": 5,
            "name": "John Test",
            "department": "IT",
            "salary": "abc",
            "join_date": "2026-08-01",
            "reason": "Non-numeric salary"
        }
    ]

    output_file = tmp_path / "rejected.csv"

    write_rejected_csv(
        rejected_rows,
        output_file
    )

    assert output_file.exists()

    with open(
        output_file,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        rows = list(reader)

    assert len(rows) == 1
    assert rows[0]["name"] == "John Test"
    assert rows[0]["reason"] == "Non-numeric salary"


# ---------------------------------------------------------
# Test 10: Blank Row
# ---------------------------------------------------------

def test_blank_row():

    row = {
        "name": "",
        "department": "",
        "salary": "",
        "join_date": ""
    }

    seen_rows = set()

    is_valid, reason = validate_row(
        row,
        seen_rows
    )

    assert is_valid is False
    assert reason == "Blank row"