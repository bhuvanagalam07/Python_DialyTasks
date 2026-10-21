import json
import logging
import os
import time
from datetime import datetime

import requests
from requests.adapters import HTTPAdapter
import urllib3.util.retry

# Load environment variables (python-dotenv is optional; defaults are used if missing)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


# --------------------------------------------------
# Configuration
# --------------------------------------------------

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "60"))
MONITOR_DURATION = int(os.getenv("MONITOR_DURATION", "600"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

# Output files (kept separate so one never overwrites the other)
MONITOR_RESULTS_FILE = "api_data.json"
PUBLIC_API_FILE = "public_api_data.json"


URLS = [
    "https://www.google.com",
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://example.com",
]


# --------------------------------------------------
# Logging configuration
# --------------------------------------------------

logging.basicConfig(
    filename="downtime.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# --------------------------------------------------
# Create requests session with retries
# --------------------------------------------------

def create_session():
    """
    Create a requests session with automatic retries.
    """

    retry_strategy = urllib3.util.retry.Retry(
        total=MAX_RETRIES,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"]
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    session = requests.Session()

    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


# --------------------------------------------------
# Check one URL
# --------------------------------------------------

def check_url(session, url):
    """
    Check URL status and response time.
    """

    start_time = time.perf_counter()

    try:
        response = session.get(
            url,
            timeout=REQUEST_TIMEOUT
        )

        response_time = time.perf_counter() - start_time

        status_code = response.status_code

        if response.ok:
            status = "UP"
        else:
            status = "DOWN"

            logging.error(
                "URL: %s | Status: %s | HTTP Code: %s | Response Time: %.3f seconds",
                url,
                status,
                status_code,
                response_time
            )

        return {
            "url": url,
            "status": status,
            "status_code": status_code,
            "response_time": round(response_time, 3)
        }

    except requests.exceptions.Timeout:

        response_time = time.perf_counter() - start_time

        logging.error(
            "URL: %s | Status: DOWN | Timeout | Response Time: %.3f seconds",
            url,
            response_time
        )

        return {
            "url": url,
            "status": "DOWN",
            "status_code": None,
            "response_time": round(response_time, 3),
            "error": "Timeout"
        }

    except requests.exceptions.RequestException as error:

        response_time = time.perf_counter() - start_time

        logging.error(
            "URL: %s | Status: DOWN | Error: %s | Response Time: %.3f seconds",
            url,
            error,
            response_time
        )

        return {
            "url": url,
            "status": "DOWN",
            "status_code": None,
            "response_time": round(response_time, 3),
            "error": str(error)
        }


# --------------------------------------------------
# Monitor all URLs
# --------------------------------------------------

def monitor_urls(session):
    """
    Check all configured URLs.
    """

    results = []

    print("\n" + "=" * 70)
    print(f"API MONITOR - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    for url in URLS:

        result = check_url(session, url)

        results.append(result)

        if result["status"] == "UP":
            print(
                f"[UP]   {url} | "
                f"HTTP {result['status_code']} | "
                f"{result['response_time']} sec"
            )

        else:
            error_message = result.get("error", "")

            print(
                f"[DOWN] {url} | "
                f"HTTP {result.get('status_code')} | "
                f"{error_message}"
            )

    return results


# --------------------------------------------------
# Save results to JSON
# --------------------------------------------------

def save_results(results):
    """
    Save monitoring results to JSON.
    """

    report = {
        "checked_at": datetime.now().isoformat(),
        "results": results
    }

    with open(MONITOR_RESULTS_FILE, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)


# --------------------------------------------------
# Fetch data from public API
# --------------------------------------------------

def fetch_public_api():
    """
    Fetch sample data from JSONPlaceholder
    and save it to public_api_data.json.
    """

    url = "https://jsonplaceholder.typicode.com/posts/1"

    try:

        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

        with open(PUBLIC_API_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print(f"\nPublic API data saved to {PUBLIC_API_FILE}")

        return data

    except requests.exceptions.RequestException as error:

        print(f"\nPublic API request failed: {error}")

        logging.error(
            "Public API failed: %s",
            error
        )

        return None


# --------------------------------------------------
# Main monitor
# --------------------------------------------------

def main():

    print("Starting API Monitor...")

    print(f"Check interval : {CHECK_INTERVAL} seconds")
    print(f"Monitor time   : {MONITOR_DURATION} seconds")
    print(f"Timeout        : {REQUEST_TIMEOUT} seconds")
    print(f"Max retries    : {MAX_RETRIES}")

    # Fetch public API once
    fetch_public_api()

    session = create_session()

    start_time = time.time()

    while time.time() - start_time < MONITOR_DURATION:

        results = monitor_urls(session)

        save_results(results)

        elapsed = time.time() - start_time

        remaining = MONITOR_DURATION - elapsed

        print(
            f"\nMonitoring continues. "
            f"Remaining time: {max(0, int(remaining))} seconds"
        )

        if remaining <= 0:
            break

        sleep_time = min(CHECK_INTERVAL, remaining)

        print(f"Next check in {int(sleep_time)} seconds...")

        time.sleep(sleep_time)

    print("\nAPI monitoring completed.")


# --------------------------------------------------
# Program entry point
# --------------------------------------------------

if __name__ == "__main__":
    main()