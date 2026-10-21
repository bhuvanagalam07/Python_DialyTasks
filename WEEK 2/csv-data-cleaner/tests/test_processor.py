
import csv
import json

import pytest

from processor import process_csv
from validator import validate_headers, validate_row


def create_csv(path, headers, rows):
    """Create a small CSV fixture for a test."""
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def test_valid_row():
    row = {
        "name": "Rahul",
        "email": "rahul@example.com",
        "age": "25",
    }
    assert validate_row(row) == []


def test_invalid_email_and_age():
    row = {
        "name": "Amit",
        "email": "not-an-email",
        "age": "abc",
    }
    errors = validate_row(row)

    assert "Invalid email format" in errors
    assert "Age must be an integer" in errors


def test_missing_required_column():
    with pytest.raises(ValueError, match="Missing required columns"):
        validate_headers(["name", "email"])


def test_duplicate_headers():
    with pytest.raises(ValueError, match="duplicate column"):
        validate_headers(["name", "email", "email", "age"])


def test_process_csv_counts_and_outputs(tmp_path):
    input_file = tmp_path / "input.csv"
    output_dir = tmp_path / "output"

    create_csv(
        input_file,
        ["name", "email", "age"],
        [
            {"name": "Rahul", "email": "rahul@example.com", "age": "25"},
            {"name": "Priya", "email": "priya@example.com", "age": "30"},
            {"name": "Amit", "email": "bad-email", "age": "abc"},
            {"name": "Rahul", "email": "rahul@example.com", "age": "25"},
        ],
    )

    summary = process_csv(input_file, output_dir)

    assert summary["total_rows"] == 4
    assert summary["valid_rows"] == 2
    assert summary["invalid_rows"] == 1
    assert summary["duplicate_rows"] == 1

    with (output_dir / "cleaned.csv").open(
        encoding="utf-8", newline=""
    ) as file:
        cleaned = list(csv.DictReader(file))

    assert len(cleaned) == 2
    assert cleaned[0]["name"] == "Rahul"
    assert cleaned[1]["name"] == "Priya"

    with (output_dir / "invalid_rows.csv").open(
        encoding="utf-8", newline=""
    ) as file:
        invalid = list(csv.DictReader(file))

    assert len(invalid) == 1
    assert "Invalid email format" in invalid[0]["error_reason"]
    assert "Age must be an integer" in invalid[0]["error_reason"]

    saved_summary = json.loads(
        (output_dir / "summary.json").read_text(encoding="utf-8")
    )
    assert saved_summary == summary


def test_nonexistent_input_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        process_csv(tmp_path / "missing.csv", tmp_path / "output")


def test_empty_file(tmp_path):
    input_file = tmp_path / "empty.csv"
    input_file.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="empty or has no header"):
        process_csv(input_file, tmp_path / "output")


def test_missing_columns_in_input(tmp_path):
    input_file = tmp_path / "wrong_columns.csv"
    create_csv(
        input_file,
        ["name", "email"],
        [{"name": "Rahul", "email": "rahul@example.com"}],
    )

    with pytest.raises(ValueError, match="Missing required columns"):
        process_csv(input_file, tmp_path / "output")


def test_empty_values_are_rejected(tmp_path):
    input_file = tmp_path / "missing_age.csv"
    create_csv(
        input_file,
        ["name", "email", "age"],
        [{"name": "Rahul", "email": "rahul@example.com", "age": ""}],
    )

    summary = process_csv(input_file, tmp_path / "output")

    assert summary["invalid_rows"] == 1
    assert summary["valid_rows"] == 0
