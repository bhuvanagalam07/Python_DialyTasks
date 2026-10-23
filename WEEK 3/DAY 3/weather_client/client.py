"""HTTP adapter (timeouts, safe retries, status validation) + WeatherClient.

Assumed API (adapt paths to your provider):
  GET /v1/locations/{city}/current
  GET /v1/locations/{city}/history?page=N&page_size=M -> {"items": [...], "next_page": int|null}
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Any, Callable, Mapping
from urllib.parse import quote

import requests

from .exceptions import (ApiConnectionError, ApiError, ApiStatusError, ApiTimeoutError,
                         MalformedResponseError, PaginationLimitError)
from .validators import Observation, validate_observation, validate_page

log = logging.getLogger(__name__)
DEFAULT_TIMEOUT = (3.05, 10.0)  # (connect, read) seconds


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3          # total tries including the first
    backoff_base: float = 0.5      # doubles each retry
    backoff_max: float = 5.0       # cap for any single sleep
    retry_statuses: frozenset = frozenset({429, 502, 503, 504})

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be >= 1")
        if self.backoff_base < 0 or self.backoff_max < 0:
            raise ValueError("backoff values must be >= 0")

    def delay_for(self, attempt: int, retry_after: float | None = None) -> float:
        if retry_after is not None:
            return min(retry_after, self.backoff_max)
        return min(self.backoff_base * 2 ** (attempt - 1), self.backoff_max)


def _retry_after(value: str | None) -> float | None:
    try:
        seconds = float(value) if value is not None else None
    except ValueError:
        return None  # HTTP-date form not supported
    return seconds if seconds is not None and seconds >= 0 else None


class HttpAdapter:
    """GET-only (idempotent) adapter, so retrying is always safe."""

    def __init__(self, base_url: str, *, timeout=DEFAULT_TIMEOUT, retry: RetryPolicy | None = None,
                 session: requests.Session | None = None,
                 sleep: Callable[[float], None] = time.sleep,
                 headers: Mapping[str, str] | None = None) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._retry = retry or RetryPolicy()
        self._session = session or requests.Session()
        self._sleep = sleep  # injectable: tests never really sleep
        if headers:
            self._session.headers.update(headers)

    def get_json(self, path: str, params: Mapping[str, Any] | None = None) -> Any:
        url = f"{self._base_url}/{path.lstrip('/')}"
        policy = self._retry
        last: ApiError | None = None

        for attempt in range(1, policy.max_attempts + 1):
            retry_after = None
            try:
                resp = self._session.get(url, params=params, timeout=self._timeout)
            except requests.exceptions.Timeout as exc:  # first: ConnectTimeout is both
                last = ApiTimeoutError(f"timeout calling {url}: {exc}")
            except requests.exceptions.ConnectionError as exc:
                last = ApiConnectionError(f"connection error calling {url}: {exc}")
            except requests.exceptions.RequestException as exc:
                raise ApiError(f"request failed for {url}: {exc}") from exc  # not retried
            else:
                status = resp.status_code
                if 200 <= status < 300:
                    try:
                        return resp.json()
                    except ValueError as exc:
                        raise MalformedResponseError(f"invalid JSON from {url}") from exc
                err = ApiStatusError(status, (resp.text or "")[:200], attempts=attempt)
                if status not in policy.retry_statuses:
                    raise err  # permanent failure: fail fast
                last = err
                retry_after = _retry_after(resp.headers.get("Retry-After"))

            if attempt == policy.max_attempts:
                break
            delay = policy.delay_for(attempt, retry_after)
            log.warning("attempt %d/%d failed (%s); retrying in %.2fs",
                        attempt, policy.max_attempts, last, delay)
            self._sleep(delay)

        if isinstance(last, ApiStatusError):
            last.attempts = policy.max_attempts
        raise last  # type: ignore[misc]


class WeatherClient:
    def __init__(self, adapter: HttpAdapter, *, max_pages: int = 5,
                 max_items: int = 500, page_size: int = 50) -> None:
        if min(max_pages, max_items, page_size) < 1:
            raise ValueError("max_pages, max_items and page_size must be >= 1")
        self._http = adapter
        self._max_pages, self._max_items, self._page_size = max_pages, max_items, page_size

    @staticmethod
    def _city_path(city: str) -> str:
        city = (city or "").strip()
        if not city:
            raise ValueError("city must be a non-empty string")
        return f"/v1/locations/{quote(city, safe='')}"

    def current(self, city: str) -> Observation:
        return validate_observation(self._http.get_json(f"{self._city_path(city)}/current"))

    def history(self, city: str) -> list[Observation]:
        """All pages, bounded by max_pages/max_items (raises PaginationLimitError)."""
        path = f"{self._city_path(city)}/history"
        results: list[Observation] = []
        page: int | None = 1
        fetched = 0
        while page is not None:
            if fetched >= self._max_pages:
                raise PaginationLimitError(f"more data after {self._max_pages} pages (max_pages reached)")
            payload = self._http.get_json(path, params={"page": page, "page_size": self._page_size})
            items, page = validate_page(payload, page)
            results.extend(validate_observation(i) for i in items)
            if len(results) > self._max_items:
                raise PaginationLimitError(f"more than max_items={self._max_items} items")
            fetched += 1
        return results
