"""Create JSON and CSV reports from processed employee data."""
import csv
import json
from collections import defaultdict
from pathlib import Path

from .models import ProcessingResult

def build_department_summary(result: ProcessingResult) -> list[dict[str, object]]:
    departments: dict[str, list[float]] = defaultdict(list)
    for employee in result.valid_employees:
        departments[employee.department].append(employee.salary)

    summary = []
    for department, salaries in sorted(departments.items()):
        summary.append({
            "department": department,
            "headcount": len(salaries),
            "average_salary": round(sum(salaries) / len(salaries), 2),
        })
    return summary

def write_reports(result: ProcessingResult, output_dir: Path) -> list[Path]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    employee_report = output_dir / "employee_report.json"
    department_summary = output_dir / "department_summary.csv"
    rejected_report = output_dir / "rejected.csv"

    employees = [{
        "name": employee.name,
        "department": employee.department,
        "salary": employee.salary,
        "join_date": employee.join_date.isoformat(),
    } for employee in result.valid_employees]

    with employee_report.open("w", encoding="utf-8") as handle:
        json.dump({"employees": employees, "total_valid": len(employees)}, handle, indent=2)

    summary = build_department_summary(result)
    with department_summary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["department", "headcount", "average_salary"])
        writer.writeheader()
        writer.writerows(summary)

    with rejected_report.open("w", newline="", encoding="utf-8") as handle:
        fields = ["row_number", "reason", "name", "department", "salary", "join_date"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(result.rejected_rows)

    return [employee_report, department_summary, rejected_report]
