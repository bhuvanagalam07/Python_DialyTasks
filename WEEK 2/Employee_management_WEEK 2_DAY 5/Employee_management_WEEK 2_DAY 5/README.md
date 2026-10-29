# Employee Data Processor

A beginner-friendly Python CLI mini-project that reads employee data from CSV, validates records, logs processing activity, and creates CSV/JSON reports.

## Features

- Reusable Python package and command-line interface (`argparse`)
- CSV input using the standard library
- Validation for names, departments, non-negative numeric salaries, and ISO dates (`YYYY-MM-DD`)
- Invalid records are written to `rejected.csv` instead of stopping all processing
- Logging to a file
- JSON employee report and department-wise CSV summary
- Automated tests with `pytest`

## Requirements

- Python 3.10 or newer
- `pip`

## Setup

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, use `python -m pip install -r requirements.txt` without activating the environment, or use Command Prompt activation: `.venv\\Scripts\\activate.bat`.

## Run

From the project root:

```powershell
python main.py
```

Choose your own paths:

```powershell
python main.py --input data/employees.csv --output-dir reports --log logs/app.log
```

Exit code is `0` for success and `1` for a handled processing error.

## Test

```powershell
python -m pytest -v
```

## Output files

- `reports/employee_report.json`: valid employee records
- `reports/department_summary.csv`: headcount and average salary by department
- `reports/rejected.csv`: invalid rows and rejection reasons
- `logs/app.log`: processing activity and errors

The sample CSV intentionally includes invalid salary values to demonstrate validation and rejected-row reporting.

## Demo script (about 1 minute)

1. Show `data/employees.csv` and point out the valid and invalid rows.
2. Run `python main.py`.
3. Show the valid/rejected counts in the terminal.
4. Open the generated JSON, department summary, rejected CSV, and log file.
5. Run `python -m pytest -v` and show that the tests pass.

## Learning outcomes

This project practices modules/packages, data structures, functions, classes and dataclasses, exception handling, file operations, CSV/JSON, logging, command-line arguments, and automated tests.
