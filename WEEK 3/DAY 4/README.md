# Weather Information Client — pytest and CI

## Objective

Test a Python weather API client using pytest, reusable fixtures, parametrized tests, and GitHub Actions CI.

## Requirements

- Python 3.12 or a compatible Python version
- pip
- Git

## Setup

Create and activate a virtual environment, then install dependencies.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run the tests

```bash
python -m pytest
```

## Test coverage

- Successful weather responses
- Invalid city names
- Invalid timeout and base URL values
- HTTP errors and request timeouts
- Invalid JSON responses
- Missing required response fields
- Unexpected response data types
- Request parameters and configured timeout

## Design decisions

- Fixtures reduce duplicated test setup.
- Parametrized tests check multiple input values.
- Fake HTTP sessions prevent live network calls.
- CI runs the same test command on a clean checkout.

## Known limitations

- The client does not connect to a real weather provider in this example.
- Retry logic and pagination are not implemented here.
- Tests validate client behavior, not the availability or accuracy of a weather service.
- Dependency versions should be pinned for reproducible builds.

## Git commit

```bash
git add src tests .github requirements.txt pytest.ini .gitignore README.md
git commit -m "test: add pytest fixtures and CI workflow"
git push origin main
```

Replace `main` with your current branch name if needed.
