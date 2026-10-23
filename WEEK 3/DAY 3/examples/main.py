"""Run the client.

Real API:   set WEATHER_API_BASE_URL (and optionally WEATHER_API_KEY) in .env, then
            python examples/main.py London
No base URL: runs an offline demo with mocked HTTP (success + failure cases).
"""
import logging
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from weather_client import ApiError, HttpAdapter, RetryPolicy, WeatherClient  # noqa: E402

logging.basicConfig(level=logging.WARNING, format="  log: %(message)s")


def run_real(city: str) -> int:
    headers = {"Authorization": f"Bearer {os.environ['WEATHER_API_KEY']}"} \
        if os.getenv("WEATHER_API_KEY") else None
    adapter = HttpAdapter(
        os.environ["WEATHER_API_BASE_URL"],
        timeout=(float(os.getenv("WEATHER_TIMEOUT_CONNECT", 3.05)),
                 float(os.getenv("WEATHER_TIMEOUT_READ", 10))),
        retry=RetryPolicy(max_attempts=int(os.getenv("WEATHER_MAX_ATTEMPTS", 3))),
        headers=headers)
    try:
        print(WeatherClient(adapter).current(city))
        return 0
    except ApiError as exc:
        print(f"{type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


def run_offline_demo() -> int:
    import requests
    import responses

    base = "https://api.weather.test"
    cur = f"{base}/v1/locations/London/current"
    his = f"{base}/v1/locations/London/history"
    ok = {"city": "London", "timestamp": "2026-10-21T10:00:00Z",
          "temperature_c": 14.5, "condition": "Cloudy"}

    def client(**kw):
        return WeatherClient(HttpAdapter(base, retry=RetryPolicy(max_attempts=3),
                                         sleep=lambda s: None), **kw)

    def scenario(title, setup, action):
        print(f"\n== {title}")
        with responses.RequestsMock() as rsps:
            setup(rsps)
            try:
                print("  OK:", action())
            except ApiError as exc:
                print(f"  FAILED as expected -> {type(exc).__name__}: {exc}")

    scenario("Success", lambda r: r.get(cur, json=ok), lambda: client().current("London"))
    scenario("503 then success (retry)",
             lambda r: (r.get(cur, status=503), r.get(cur, json=ok)), lambda: client().current("London"))
    scenario("404 (not retried)", lambda r: r.get(cur, status=404), lambda: client().current("London"))
    scenario("Timeouts exhausted",
             lambda r: [r.get(cur, body=requests.exceptions.ReadTimeout("slow")) for _ in range(3)],
             lambda: client().current("London"))
    scenario("Malformed JSON", lambda r: r.get(cur, body="<html>"), lambda: client().current("London"))
    scenario("Pagination limit (max_pages=2)",
             lambda r: (r.get(his, json={"items": [ok], "next_page": 2}),
                        r.get(his, json={"items": [ok], "next_page": 3})),
             lambda: client(max_pages=2).history("London"))
    return 0


if __name__ == "__main__":
    if os.getenv("WEATHER_API_BASE_URL"):
        raise SystemExit(run_real(sys.argv[1] if len(sys.argv) > 1 else "London"))
    raise SystemExit(run_offline_demo())
