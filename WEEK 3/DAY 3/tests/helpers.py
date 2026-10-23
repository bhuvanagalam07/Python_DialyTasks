from weather_client import HttpAdapter, RetryPolicy, WeatherClient

BASE = "https://api.weather.test"
CUR = f"{BASE}/v1/locations/London/current"
HIS = f"{BASE}/v1/locations/London/history"


def obs(temp=14.5, **over):
    return {"city": "London", "timestamp": "2026-10-21T10:00:00Z",
            "temperature_c": temp, "condition": "Cloudy", **over}


def make_client(sleeps, *, max_attempts=3, **kw):
    adapter = HttpAdapter(BASE, retry=RetryPolicy(max_attempts=max_attempts, backoff_base=0.5,
                                                  backoff_max=2.0), sleep=sleeps.append)
    return WeatherClient(adapter, **kw)
