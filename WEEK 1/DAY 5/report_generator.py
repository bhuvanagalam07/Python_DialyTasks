import csv
import json
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import date, timedelta
from pathlib import Path


@dataclass
class Employee:
    """One employee record."""

    name: str
    department: str
    salary: float
    join_date: str


class ReportGenerator:
    """Generate JSON employee details and department CSV summaries."""

    def __init__(self, input_file: str | Path):
        self.input_file = Path(input_file)

    def read_employees(self) -> list[Employee]:
        if not self.input_file.is_file():
            raise FileNotFoundError(f"Employee file not found: {self.input_file}")

        employees = []
        with self.input_file.open("r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            required = {"name", "department", "salary", "join_date"}
            if not required.issubset(set(reader.fieldnames or [])):
                raise ValueError("CSV must contain name, department, salary, join_date")

            for row in reader:
                try:
                    employee = Employee(
                        name=row["name"].strip(),
                        department=row["department"].strip(),
                        salary=float(row["salary"]),
                        join_date=row["join_date"].strip(),
                    )
                except (ValueError, AttributeError) as exc:
                    raise ValueError(f"Invalid employee record: {row}") from exc

                if not employee.name or not employee.department:
                    raise ValueError("Name and department cannot be empty")
                try:
                    date.fromisoformat(employee.join_date)
                except ValueError as exc:
                    raise ValueError(
                        f"Invalid join date: {employee.join_date}"
                    ) from exc
                if employee.salary < 0:
                    raise ValueError("Salary cannot be negative")
                employees.append(employee)
        return employees

    def generate(self, output_dir: str | Path = "reports") -> dict:
        employees = self.read_employees()
        output = Path(output_dir)
        output.mkdir(parents=True, exist_ok=True)

        departments = defaultdict(lambda: {"employee_count": 0, "total_salary": 0.0})
        for employee in employees:
            department = departments[employee.department]
            department["employee_count"] += 1
            department["total_salary"] += employee.salary

        department_report = []
        for name, values in sorted(departments.items()):
            count = values["employee_count"]
            total = round(values["total_salary"], 2)
            department_report.append(
                {
                    "department": name,
                    "employee_count": count,
                    "total_salary": total,
                    "average_salary": round(total / count, 2),
                }
            )

        report = {
            "total_employees": len(employees),
            "employees": [asdict(employee) for employee in employees],
            "departments": department_report,
        }
        with (output / "employee_report.json").open("w", encoding="utf-8") as file:
            json.dump(report, file, indent=4)

        with (output / "department_summary.csv").open(
            "w", newline="", encoding="utf-8"
        ) as file:
            fields = ["department", "employee_count", "total_salary", "average_salary"]
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(department_report)

        print(f"Total employees: {len(employees)}")
        print(f"JSON report: {output / 'employee_report.json'}")
        print(f"Department report: {output / 'department_summary.csv'}")
        return report

    # ----- methods used by tests/test_report.py and toolkit.py -----

    def load_employees(self) -> list[dict]:
        """Return employees as dictionaries."""
        return [asdict(employee) for employee in self.read_employees()]

    def department_statistics(self) -> dict:
        """Return {department: {employee_count, average_salary}}."""
        totals = defaultdict(lambda: {"employee_count": 0, "total": 0.0})
        for employee in self.read_employees():
            totals[employee.department]["employee_count"] += 1
            totals[employee.department]["total"] += employee.salary

        return {
            name: {
                "employee_count": values["employee_count"],
                "average_salary": round(values["total"] / values["employee_count"], 2),
            }
            for name, values in sorted(totals.items())
        }

    def generate_report(self, output_file: str | Path) -> dict:
        """Write the JSON report to output_file and return it."""
        employees = self.load_employees()
        cutoff = date.today() - timedelta(days=90)

        report = {
            "total_employees": len(employees),
            "department_statistics": self.department_statistics(),
            "employees_joined_last_90_days": [
                employee
                for employee in employees
                if date.fromisoformat(employee["join_date"]) >= cutoff
            ],
        }

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as file:
            json.dump(report, file, indent=4)

        return report
