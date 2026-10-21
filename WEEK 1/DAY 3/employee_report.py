    import csv
import json
import os
from pathlib import Path
from datetime import datetime, timedelta


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

BASE_DIR = Path(__file__).parent

INPUT_FILE = BASE_DIR / "employees.csv"
OUTPUT_CSV = BASE_DIR / "employees_report.csv"
OUTPUT_JSON = BASE_DIR / "employees_report.json"
REJECTED_CSV = BASE_DIR / "rejected.csv"


REQUIRED_COLUMNS = {
    "name",
    "department",
    "salary",
    "join_date"
}


# ---------------------------------------------------------
# Date Utilities
# ---------------------------------------------------------

def parse_date(date_text):
    """
    Convert a YYYY-MM-DD string into a datetime object.

    Returns:
        datetime object if valid
        None if the date is invalid
    """

    try:
        return datetime.strptime(date_text.strip(), "%Y-%m-%d")
    except (ValueError, AttributeError):
        return None


# ---------------------------------------------------------
# Row Validation
# ---------------------------------------------------------

def validate_row(row, seen_rows):
    """
    Validate one employee row.

    Returns:
        (True, "") if valid
        (False, reason) if invalid
    """

    # Check for completely blank row
    if not any(value and value.strip() for value in row.values()):
        return False, "Blank row"

    # Check missing values
    for column in REQUIRED_COLUMNS:
        value = row.get(column, "")

        if value is None or not value.strip():
            return False, f"Missing value: {column}"

    # Validate salary
    salary_text = row["salary"].strip()

    try:
        float(salary_text)
    except ValueError:
        return False, "Non-numeric salary"

    # Validate join date
    join_date = parse_date(row["join_date"])

    if join_date is None:
        return False, "Invalid date format. Expected YYYY-MM-DD"

    # Detect duplicate rows
    row_key = (
        row["name"].strip().lower(),
        row["department"].strip().lower(),
        row["salary"].strip(),
        row["join_date"].strip()
    )

    if row_key in seen_rows:
        return False, "Duplicate row"

    seen_rows.add(row_key)

    return True, ""


# ---------------------------------------------------------
# Read Employee CSV
# ---------------------------------------------------------

def read_employees(file_path):
    """
    Read employees from CSV.

    Returns:
        valid employees
        rejected employees
    """

    valid_employees = []
    rejected_employees = []

    seen_rows = set()

    try:
        with open(file_path, "r", newline="", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            # Check CSV headers
            if reader.fieldnames is None:
                raise ValueError("CSV file has no header")

            actual_columns = set(reader.fieldnames)

            missing_columns = REQUIRED_COLUMNS - actual_columns

            if missing_columns:
                raise ValueError(
                    f"Missing required columns: {missing_columns}"
                )

            for row_number, row in enumerate(reader, start=2):

                is_valid, reason = validate_row(
                    row,
                    seen_rows
                )

                if is_valid:

                    employee = {
                        "name": row["name"].strip(),
                        "department": row["department"].strip(),
                        "salary": float(row["salary"].strip()),
                        "join_date": row["join_date"].strip()
                    }

                    valid_employees.append(employee)

                else:

                    rejected_employees.append({
                        "row_number": row_number,
                        "name": row.get("name", ""),
                        "department": row.get("department", ""),
                        "salary": row.get("salary", ""),
                        "join_date": row.get("join_date", ""),
                        "reason": reason
                    })

    except FileNotFoundError:

        print(f"Error: Input file not found: {file_path}")

    except Exception as error:

        print(f"Error while reading CSV: {error}")

    return valid_employees, rejected_employees


# ---------------------------------------------------------
# Department-wise Statistics
# ---------------------------------------------------------

def department_statistics(employees):
    """
    Calculate department-wise headcount
    and average salary.
    """

    departments = {}

    for employee in employees:

        department = employee["department"]

        if department not in departments:
            departments[department] = {
                "headcount": 0,
                "total_salary": 0
            }

        departments[department]["headcount"] += 1
        departments[department]["total_salary"] += employee["salary"]

    statistics = {}

    for department, data in departments.items():

        average_salary = (
            data["total_salary"] / data["headcount"]
        )

        statistics[department] = {
            "headcount": data["headcount"],
            "average_salary": round(average_salary, 2)
        }

    return statistics


# ---------------------------------------------------------
# Employees Joined in Last 90 Days
# ---------------------------------------------------------

def employees_joined_last_90_days(employees):
    """
    Find employees who joined within the last 90 days.
    """

    today = datetime.today()

    ninety_days_ago = today - timedelta(days=90)

    recent_employees = []

    for employee in employees:

        join_date = parse_date(employee["join_date"])

        if ninety_days_ago <= join_date <= today:

            recent_employees.append(employee)

    return recent_employees


# ---------------------------------------------------------
# Export Rejected Rows
# ---------------------------------------------------------

def write_rejected_csv(rejected_employees, file_path):
    """
    Write invalid records to rejected.csv.
    """

    fieldnames = [
        "row_number",
        "name",
        "department",
        "salary",
        "join_date",
        "reason"
    ]

    with open(
        file_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(rejected_employees)


# ---------------------------------------------------------
# Export Employee Report to CSV
# ---------------------------------------------------------

def write_report_csv(employees, statistics, file_path):
    """
    Write employee report to CSV.
    """

    with open(
        file_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Department",
            "Headcount",
            "Average Salary"
        ])

        for department, data in sorted(statistics.items()):

            writer.writerow([
                department,
                data["headcount"],
                data["average_salary"]
            ])


# ---------------------------------------------------------
# Export Report to JSON
# ---------------------------------------------------------

def write_report_json(
    employees,
    statistics,
    recent_employees,
    file_path
):
    """
    Write complete report to JSON.
    """

    report = {
        "total_valid_employees": len(employees),
        "total_rejected_rows": 0,
        "department_statistics": statistics,
        "employees_joined_last_90_days": recent_employees
    }

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4
        )


# ---------------------------------------------------------
# Batch Processing
# ---------------------------------------------------------

def find_csv_files(folder):
    """
    Find every CSV file inside a folder.
    """

    folder = Path(folder)

    return [
        file
        for file in folder.glob("*.csv")
        if file.name != "rejected.csv"
        and file.name != "employees_report.csv"
    ]


# ---------------------------------------------------------
# Display Report
# ---------------------------------------------------------

def display_report(
    employees,
    rejected,
    statistics,
    recent_employees
):

    print("\n" + "=" * 50)
    print("EMPLOYEE REPORT")
    print("=" * 50)

    print(f"\nValid employees   : {len(employees)}")
    print(f"Rejected rows     : {len(rejected)}")

    print("\nDepartment Statistics")
    print("-" * 50)

    for department, data in sorted(statistics.items()):

        print(
            f"{department:<15} "
            f"Headcount: {data['headcount']:<5} "
            f"Average Salary: ₹{data['average_salary']}"
        )

    print("\nEmployees Joined in Last 90 Days")
    print("-" * 50)

    if recent_employees:

        for employee in recent_employees:

            print(
                f"{employee['name']} - "
                f"{employee['department']} - "
                f"{employee['join_date']}"
            )

    else:

        print("No employees joined in the last 90 days.")

    print("\nOutput Files")
    print("-" * 50)

    print(f"CSV Report : {OUTPUT_CSV}")
    print(f"JSON Report: {OUTPUT_JSON}")
    print(f"Rejected   : {REJECTED_CSV}")


# ---------------------------------------------------------
# Main Function
# ---------------------------------------------------------

def main():

    print("Starting Employee Report...")

    # Check input file
    if not os.path.exists(INPUT_FILE):

        print(f"Input file does not exist: {INPUT_FILE}")
        return

    # Read and validate employees
    employees, rejected = read_employees(
        INPUT_FILE
    )

    # Department statistics
    statistics = department_statistics(
        employees
    )

    # Employees joined in last 90 days
    recent_employees = employees_joined_last_90_days(
        employees
    )

    # Write rejected rows
    write_rejected_csv(
        rejected,
        REJECTED_CSV
    )

    # Write CSV report
    write_report_csv(
        employees,
        statistics,
        OUTPUT_CSV
    )

    # Write JSON report
    write_report_json(
        employees,
        statistics,
        recent_employees,
        OUTPUT_JSON
    )

    # Display results
    display_report(
        employees,
        rejected,
        statistics,
        recent_employees
    )

    print("\nEmployee report completed successfully.")


# ---------------------------------------------------------
# Program Entry Point
# ---------------------------------------------------------

if __name__ == "__main__":
    main()