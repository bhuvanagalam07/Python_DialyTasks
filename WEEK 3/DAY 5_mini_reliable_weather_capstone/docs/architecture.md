# Architecture and data contract

## Flow

`CLI (main.py) -> source selection -> API adapter or sample JSON -> validator -> collection processor -> JSON/CSV report generator`

The CLI is responsible for orchestration and user-facing exit codes. `WeatherApiClient` owns HTTP details and bounded retries. The validator enforces the record contract. The processor applies deterministic calculations. The report generator owns file output.

## Record contract

Each record is a JSON object with:

- `city`: non-empty string; city names must be unique, case-insensitively.
- `temperature`: finite numeric value from -100 through 70 Celsius (booleans are rejected).

Input is a non-empty JSON list of records. Invalid records fail the run rather than silently changing the results.

## Report contract

`weather_report.json` contains the summary, records, source label, and UTC generation timestamp. `weather_report.csv` contains one row per city with `city` and `temperature` columns.

## Design decisions

- The default run uses bundled sample data, so the application and tests work without network access.
- Live mode uses Open-Meteo and requires internet access.
- HTTP requests have a timeout. Only transient connection/time-out errors and server-side HTTP errors are retried, with a finite retry limit.
- Tests mock network calls and use temporary files, so results are deterministic.
