# Failure and recovery notes

| Failure | Behavior | Recovery |
|---|---|---|
| Input file missing | Clear error and exit code 1; no report is claimed | Check `--input` path or use bundled default sample data |
| Invalid JSON | Clear validation error and exit code 1 | Correct the JSON syntax |
| Invalid record / duplicate city | Validation error; processing stops | Correct the city or temperature value |
| API timeout / connection issue | Bounded retries, then controlled API error and exit code 1 | Check connectivity or rerun later |
| HTTP 5xx | Bounded retry, then controlled error | Retry later; inspect provider status if persistent |
| Malformed API response | Controlled error; no report generated from invalid data | Check endpoint/schema and update adapter contract if needed |
| Report directory/write failure | `ReportError` with a clear message | Choose a writable `--output-dir` |

## Operational notes

The program does not silently substitute sample data when live mode fails. This prevents stale/sample values from being mistaken for live observations. No credentials are required by the public Open-Meteo endpoint. Do not commit `.env`, tokens, or sensitive output.
