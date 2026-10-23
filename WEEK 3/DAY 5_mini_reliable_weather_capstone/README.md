# Reliable Weather Data-Processing Utility

A small, testable Python capstone that combines an API adapter, collection processing, validation, report generation, failure handling, automated tests, and CI.

## Features

- Offline-by-default sample workflow (no API key or network needed).
- Optional live current-temperature lookup through Open-Meteo.
- Request timeouts and bounded retries for transient API failures.
- Validation for required fields, temperature range, empty input, and duplicate cities.
- JSON summary and CSV detail report.
- Logging, meaningful error messages, non-zero exit codes on failure.
- Unit and integration tests with mocked HTTP and temporary test files.
- GitHub Actions workflow.

## Requirements

Python 3.10+ recommended (CI uses Python 3.12). Windows PowerShell commands are shown below.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, run commands with `.venv\\Scripts\\python.exe` directly instead of changing execution policy.

## Run the offline demonstration

```powershell
python -m weather_processor
```

The default input is `data/sample_weather.json`. Reports are written to `reports/weather_report.json` and `reports/weather_report.csv`.

Use a custom input or output folder:

```powershell
python -m weather_processor --input data/sample_weather.json --output-dir reports
```

## Run live mode (internet required)

```powershell
python -m weather_processor --live --city Hyderabad --latitude 17.385 --longitude 78.4867
```

This uses the public Open-Meteo API. Live mode may fail if the network or provider is unavailable; the app reports the error and exits rather than mislabeling sample data as live data.

## Test and coverage

```powershell
python -m pytest -v
python -m pytest --cov=weather_processor --cov-report=term-missing
```

Tests do not call the live API. They mock HTTP behavior and use isolated temporary files.

## Example expected offline output

```text
Weather data processing completed successfully.
Data source: sample_file
Cities processed: 5
Average temperature: 29.40 C
Hottest city: Chennai (34.00 C)
Coldest city: Bengaluru (25.00 C)
JSON report: .../reports/weather_report.json
CSV report: .../reports/weather_report.csv
```

Paths vary by machine. The UTC report timestamp changes on each run.

## Failure demonstration

```powershell
python -m weather_processor --input data/missing.json
```

Expected: an `ERROR: Input file not found: ...` message and exit code 1. Other failure cases are covered by tests.

## Project structure

- `weather_processor/api_client.py`: HTTP adapter and retry policy.
- `weather_processor/validator.py`: input/data contract validation.
- `weather_processor/processor.py`: deterministic collection calculations.
- `weather_processor/report_generator.py`: JSON and CSV files.
- `weather_processor/main.py`: CLI orchestration and controlled failure behavior.
- `tests/`: unit and integration tests.
- `docs/`: architecture and recovery notes.
- `.github/workflows/tests.yml`: CI test workflow.

## Known limitations

- The bundled sample observations are demonstration data, not live weather.
- Live mode retrieves one location per invocation; it does not perform geocoding.
- The output directory must be writable. A run that fails before report generation does not create a new successful report.
- API schema changes may require updating the adapter.
