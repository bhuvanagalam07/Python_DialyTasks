# Capstone design notes

## Objective
Combine a collection processor and API adapter into a reliable workflow that emits report files and demonstrates recoverable failure behavior.

## Key choices
1. Offline sample data is the default to make a clean checkout reproducible.
2. The optional live adapter uses Open-Meteo's current temperature field and has finite timeouts/retries.
3. Validation rejects malformed records, duplicate city labels, booleans masquerading as numbers, and implausible temperature values.
4. The processing layer is pure/deterministic for the same input.
5. Report output is isolated in its own module; errors are converted into a clear application failure.
6. Network tests use mocks; filesystem tests use pytest temporary directories.

## Acceptance evidence to capture after running locally
- `python -m pytest -v` output.
- `python -m pytest --cov=weather_processor --cov-report=term-missing` output.
- Successful default CLI run and generated JSON/CSV report.
- Missing-input failure output.
- Successful GitHub Actions run after push.
- Commit hash and `git status` showing a clean working tree.

## Known limitations
This is a training capstone, not a production weather service. It does not include geocoding, persistent storage, alerting, or live multi-city batch retrieval. Live mode depends on external network/API availability.
