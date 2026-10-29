"""CSV loading, validation, and employee data processing."""
import csv
import logging
from datetime import date
from pathlib import Path

from .models import Employee, ProcessingResult

logger = logging.getLogger(__name__)
REQUIRED_COLUMNS = {"name", "department", "salary", "join_date"}

def validate_employee(row: dict[str, str], row_number: int) -> Employee:
    """Validate one CSV row and return an Employee or raise ValueError."""
    missing = REQUIRED_COLUMNS - set(row.keys())
    if missing:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")

    name = (row.get("name") or "").strip()
    department = (row.get("department") or "").strip()
    salary_text = (row.get("salary") or "").strip()
    join_date_text = (row.get("join_date") or "").strip()

    if not name:
        raise ValueError("Name cannot be empty")
    if not department:
        raise ValueError("Department cannot be empty")

    try:
        salary = float(salary_text)
    except (TypeError, ValueError) as exc:
        raise ValueError("Salary must be a number") from exc
    if salary < 0:
        raise ValueError("Salary cannot be negative")

    try:
        join_date = date.fromisoformat(join_date_text)
    except (TypeError, ValueError) as exc:
        raise ValueError("Join date must use YYYY-MM-DD format") from exc

    return Employee(name=name, department=department, salary=salary, join_date=join_date)

class EmployeeProcessor:
    """Reads employee CSV data and separates valid from rejected records."""
    def process_csv(self, input_path: Path) -> ProcessingResult:
        input_path = Path(input_path)
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        if not input_path.is_file():
            raise ValueError(f"Input path is not a file: {input_path}")

        valid: list[Employee] = []
        rejected: list[dict[str, str]] = []
        try:
            with input_path.open("r", newline="", encoding="utf-8-sig") as handle:
                reader = csv.DictReader(handle)
                if not reader.fieldnames:
                    raise ValueError("CSV file is empty or has no header")
                normalized = [name.strip() for name in reader.fieldnames if name]
                if not REQUIRED_COLUMNS.issubset(set(normalized)):
                    missing = REQUIRED_COLUMNS - set(normalized)
                    raise ValueError(f"CSV is missing required columns: {', '.join(sorted(missing))}")

                # Normalize headers so accidental spaces don't cause row validation failures.
                reader.fieldnames = normalized
                for row_number, row in enumerate(reader, start=2):
                    try:
                        employee = validate_employee(row, row_number)
                        valid.append(employee)
                    except ValueError as exc:
                        rejected.append({
                            "row_number": str(row_number),
                            "reason": str(exc),
                            "name": (row.get("name") or "").strip(),
                            "department": (row.get("department") or "").strip(),
                            "salary": (row.get("salary") or "").strip(),
                            "join_date": (row.get("join_date") or "").strip(),
                        })
                        logger.warning("Rejected CSV row %s: %s", row_number, exc)
        except UnicodeDecodeError as exc:
            raise ValueError("Input file must be UTF-8 encoded") from exc

        logger.info("Read %s valid and %s rejected rows", len(valid), len(rejected))
        return ProcessingResult(valid_employees=valid, rejected_rows=rejected)
