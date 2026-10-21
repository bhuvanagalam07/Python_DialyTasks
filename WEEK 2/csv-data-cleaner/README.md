
# CSV Data Cleaner and Validator CLI

## 1. Overview

A Python command-line application that validates employee
data stored in CSV files, removes duplicate valid records,
and generates reports.

## 2. Features

- Validates required columns: name, email, and age
- Checks required values, email format, and age range
- Normalizes whitespace and email capitalization
- Detects duplicate valid records
- Exports cleaned and invalid records
- Generates a JSON processing summary
- Logs processing events and errors
- Includes automated tests

## 3. Requirements

- Python 3.11 or later
- pytest for automated testing

## 4. Project Structure

    csv-data-cleaner/
    ├── main.py
    ├── validator.py
    ├── processor.py
    ├── logger_config.py
    ├── sample.csv
    ├── requirements.txt
    ├── README.md
    └── tests/
        └── test_processor.py

## 5. Setup

Create and activate a virtual environment.

Windows:

    python -m venv .venv
    .venv\Scripts\activate

macOS/Linux:

    python3 -m venv .venv
    source .venv/bin/activate

Install the test dependency:

    python -m pip install -r requirements.txt

## 6. Run the Application

    python main.py sample.csv --output output

The output directory contains:

- cleaned.csv: unique, valid records
- invalid_rows.csv: invalid records with reasons
- summary.json: processing counts
- app.log: application logs

## 7. Run Tests

    python -m pytest -v

## 8. Validation Rules

- Required columns: name, email, age
- Name, email, and age cannot be empty
- Email must match a basic email-format pattern
- Age must be an integer from 0 through 120
- Duplicate detection uses normalized name, email, and age
- Extra values in a row are rejected

## 9. Error Handling

The application reports missing input files, unreadable files,
malformed CSV data, invalid headers, and expected validation
errors without exposing a full traceback to the CLI user.

## 10. Limitations

Email format validation does not verify whether an address
exists. Duplicate detection is based on the combination of
name, email, and age, not email alone. Invalid records are
reported separately; duplicate records are counted and skipped.

## 11. Example

Input:

    name,email,age
    Rahul,rahul@example.com,25
    Priya,priya@example.com,30
    Amit,invalid-email,abc
    Rahul,rahul@example.com,25

Expected summary:

    Total rows:     4
    Valid rows:     2
    Invalid rows:   1
    Duplicate rows: 1
