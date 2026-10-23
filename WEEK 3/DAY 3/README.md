# Weather Client: API Client & Failure Handling

A small Python weather API client with timeouts, retries for safe transient
failures only, HTTP status validation, payload validation and bounded pagination.
All behaviour is proven with mocked HTTP tests (no network needed).

## Structure

```
weather-client-project/
├── weather_client/
│   ├── client.py        HttpAdapter + RetryPolicy + WeatherClient
│   ├── exceptions.py    ApiError hierarchy
│   └── validators.py    payload validation (observation, page)
├── tests/               client, retries, errors, validation (mocked with `responses`)
├── examples/main.py     real API run, or offline mocked demo
├── .env.example  .gitignore  requirements.txt  README.md
```

## Run

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

pytest -v                        # mocked tests
python examples/main.py          # offline demo (success + failures)

# real API (adapt paths in client.py to your provider):
cp .env.example .env             # edit values
python examples/main.py London
```

## Decisions

| Situation | Behaviour |
|---|---|
| Timeout / connection error | Retried (max 3 attempts), then `ApiTimeoutError` / `ApiConnectionError` |
| HTTP 429, 502, 503, 504 | Retried; `Retry-After` seconds honoured but capped |
| Other 4xx, and 500 | Fail fast with `ApiStatusError` (retrying can't fix them) |
| 2xx with invalid JSON / wrong shape / bad values | `MalformedResponseError`, never retried |
| Backoff | 0.5s, 1s, 2s... capped; no sleep after the last attempt |
| Pagination | Bounded by `max_pages` (5) and `max_items` (500) → `PaginationLimitError`; a non-advancing `next_page` is rejected |

Only `GET` is exposed, so retries are always safe (idempotent). Every request has a
`(3.05s connect, 10s read)` timeout by default.

## Tests

- `test_client.py`: success, URL-encoded city, multi-page, exactly `max_pages` allowed, `max_pages`/`max_items` exceeded
- `test_retries.py`: timeout then success, exhausted timeouts, 429/502/503/504, Retry-After cap, backoff cap
- `test_errors.py`: 400/401/403/404/422/500 not retried, malformed JSON, failure on page 2, base class
- `test_validation.py`: missing/wrong-type/out-of-range fields, temperature boundaries, bad cursor

## Known limitations

- API contract is an assumed placeholder; adapt paths and fields to your provider.
- No backoff jitter; `Retry-After` HTTP-date form ignored.
- Pagination raises instead of returning partial data.
- Synchronous only; no caching or circuit breaker.
