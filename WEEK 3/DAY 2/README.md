# Modular Weather Data Processor

A beginner-friendly Python project demonstrating modular design, JSON parsing,
input validation, simple domain logic, file I/O, and automated tests.

## Project structure

- `main.py` — coordinates input, parsing, validation, processing, and output.
- `parser.py` — converts JSON text to Python data and reports malformed JSON.
- `validator.py` — checks required fields, types, and humidity range.
- `processor.py` — applies simple weather-summary logic to valid records.
- `storage.py` — optional helpers for reading and writing JSON files.
- `tests/test_validator.py` — positive, negative, and boundary tests.
- `requirements.txt` — test dependency.

## Requirements

Python 3.10 or newer is recommended. The project uses only the Python standard
library at runtime; `pytest` is used for automated tests.

## Setup in VS Code (Windows PowerShell)

Open this folder in Visual Studio Code, then open Terminal > New Terminal.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, run this for the current terminal only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

## Run the application

```powershell
python main.py
```

Paste a JSON object when prompted, for example:

```json
{"city": "Visakhapatnam", "temperature": 30, "humidity": 65}
```

Expected output:

```text
Weather data validated successfully.
City: Visakhapatnam
Temperature: 30°C
Humidity: 65%
Summary: Temperature is moderate.
```

Try a missing field:

```json
{"city": "Visakhapatnam", "temperature": 30}
```

Expected error:

```text
Input error: Missing required field: humidity
```

Try malformed JSON, such as `{"city":`, to see a useful parsing error.

## Run tests

```powershell
python -m pytest -v
```

The tests cover valid data, missing fields, incorrect temperature type, invalid
humidity boundaries, empty city, and boolean temperature.

## Design decisions

- Parsing, validation, domain logic, and file operations are separated so each
  module has one clear responsibility.
- Validation runs before processing, so invalid data is not processed.
- Errors are reported in plain language rather than exposing a traceback for
  expected input errors.
- `storage.py` is an optional JSON file helper and is not called by the
  interactive `main.py` workflow.

## Known limitations

- This is a learning example, not a production weather service.
- It does not fetch live weather data from an external API.
- Temperature is checked for numeric type but not restricted to a particular
  climate range; valid extremes depend on the application.
- Unknown JSON fields are currently allowed.
- No authentication, database, or API retry logic is included.

## Git version control

After reviewing the files and confirming tests pass:

```powershell
git status
git add main.py parser.py validator.py processor.py storage.py tests README.md requirements.txt
git commit -m "feat: modular design and input validation"
```
