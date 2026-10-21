"""Data models used by the employee processor."""
from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class Employee:
    name: str
    department: str
    salary: float
    join_date: date

@dataclass
class ProcessingResult:
    valid_employees: list[Employee]
    rejected_rows: list[dict[str, str]]
