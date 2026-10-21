import json
import logging
import time
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

import requests

from models import ApiResult


class ApiMonitor:
    """Monitor API endpoints and record their status."""

    def __init__(self, timeout=5, max_retries=3):
        self.timeout = timeout
        self.max_retries = max_retries

        self.log_file = Path(__file__).parent / "downtime.log"

        self.logger = logging.getLogger("ops_toolkit.api_monitor")
        self.logger.setLevel(logging.ERROR)

        if not self.logger.handlers:
            handler = logging.FileHandler(self.log_file, encoding="utf-8")
            handler.setFormatter(
                logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
            )
            self.logger.addHandler(handler)

    def check_url(self, url):
        """Check one URL and return an ApiResult."""
        status_code = None
        error_message = None
        response_time = 0.0

        for attempt in range(self.max_retries):
            start_time = time.perf_counter()

            try:
                response = requests.get(
                    url,
                    headers={"Accept": "application/json"},
                    timeout=self.timeout,
                )

                response_time = time.perf_counter() - start_time
                status_code = response.status_code

                if 200 <= status_code < 400:
                    return ApiResult(
                        url=url,
                        status_code=status_code,
                        response_time=round(response_time, 4),
                        success=True,
                        checked_at=datetime.now(),
                    )

                error_message = f"HTTP {status_code}"

                # Retry server errors and rate limiting.
                if status_code < 500 and status_code != 429:
                    break

            except requests.exceptions.Timeout:
                response_time = time.perf_counter() - start_time
                error_message = "Request timed out"

            except requests.exceptions.RequestException as error:
                response_time = time.perf_counter() - start_time
                error_message = str(error)
                break

            if attempt < self.max_retries - 1:
                time.sleep(1)

        self.logger.error("%s | %s", url, error_message)

        return ApiResult(
            url=url,
            status_code=status_code,
            response_time=round(response_time, 4),
            success=False,
            checked_at=datetime.now(),
        )

    def load_urls(self, file_path):
        """Read URLs from a text file, skipping blank lines and # comments."""
        path = Path(file_path)

        if not path.is_file():
            raise FileNotFoundError(f"URL file not found: {path}")

        with path.open("r", encoding="utf-8-sig") as file:
            return [
                line.strip()
                for line in file
                if line.strip() and not line.strip().startswith("#")
            ]

    def monitor(self, urls):
        """Check every URL, print a status line for each, return results."""
        results = []

        print("\n===== API MONITOR =====")
        for url in urls:
            result = self.check_url(url)
            results.append(result)

            status = "UP" if result.success else "DOWN"
            print(
                f"{status:<5} {result.status_code or '-':<4} "
                f"{result.response_time:.3f}s  {url}"
            )

        return results

    def save_results(self, results, file_path):
        """Save results to a JSON file."""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        data = []
        for result in results:
            item = asdict(result)
            item["checked_at"] = result.checked_at.isoformat()
            data.append(item)

        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
