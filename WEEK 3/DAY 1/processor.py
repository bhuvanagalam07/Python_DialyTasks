"""API Monitoring - event processor.

Problem: process a stream of API call events and
  1. ignore duplicate events          (membership test)
  2. keep per-endpoint statistics     (lookup by key)
  3. track error rate of the last N seconds (FIFO sliding window)
  4. buffer alerts for a consumer     (bounded FIFO queue)

ApiProcessor   -> chosen structures: set, dict, deque      (O(1) per event)
NaiveProcessor -> baseline structures: list, list, list    (O(n) per event)
Both expose the same interface so tests/benchmarks can compare them.
"""
from collections import deque

REQUIRED_FIELDS = ("id", "endpoint", "status", "latency_ms", "timestamp")


def validate_event(event):
    """Raise ValueError if the event dict is malformed."""
    if not isinstance(event, dict):
        raise ValueError("event must be a dict")
    missing = [f for f in REQUIRED_FIELDS if f not in event]
    if missing:
        raise ValueError(f"missing fields: {missing}")
    if not event["id"] or not event["endpoint"]:
        raise ValueError("id and endpoint must be non-empty")
    if not isinstance(event["status"], int) or not 100 <= event["status"] <= 599:
        raise ValueError(f"invalid status: {event['status']!r}")
    if event["latency_ms"] < 0:
        raise ValueError("latency_ms must be >= 0")


def _new_stats():
    return {"count": 0, "errors": 0, "total_latency_ms": 0.0, "max_latency_ms": 0.0}


def _update_stats(s, event):
    s["count"] += 1
    s["errors"] += event["status"] >= 500
    s["total_latency_ms"] += event["latency_ms"]
    s["max_latency_ms"] = max(s["max_latency_ms"], event["latency_ms"])


class ApiProcessor:
    """Chosen structures. Amortised O(1) per event.

    set    -> seen ids          (O(1) membership,  O(U) space)
    dict   -> stats by endpoint (O(1) lookup,      O(E) space)
    deque  -> sliding window    (O(1) popleft,     O(W) space)
    deque(maxlen) -> alerts     (O(1) push/pop,    O(Q) bounded space)
    """

    def __init__(self, window_seconds=60, error_threshold=0.5,
                 min_events=5, queue_size=100):
        if window_seconds <= 0:
            raise ValueError("window_seconds must be > 0")
        if not 0 < error_threshold <= 1:
            raise ValueError("error_threshold must be in (0, 1]")
        if queue_size <= 0:
            raise ValueError("queue_size must be > 0")
        self.window_seconds = window_seconds
        self.error_threshold = error_threshold
        self.min_events = min_events
        self._seen = set()
        self._stats = {}
        self._window = deque()
        self._window_errors = 0
        self._last_ts = None
        self._alerting = False
        self.alerts = deque(maxlen=queue_size)
        self.dropped_alerts = 0

    def process(self, event):
        """Return 'ok' or 'duplicate'. Raise ValueError for invalid input."""
        validate_event(event)
        if self._last_ts is not None and event["timestamp"] < self._last_ts:
            raise ValueError("out-of-order timestamp")
        if event["id"] in self._seen:                       # O(1)
            return "duplicate"
        self._seen.add(event["id"])
        self._last_ts = event["timestamp"]
        _update_stats(self._stats.setdefault(event["endpoint"], _new_stats()), event)
        self._add_to_window(event)
        self._check_alert(event["timestamp"])
        return "ok"

    def _add_to_window(self, event):
        self._window.append(event)
        self._window_errors += event["status"] >= 500
        cutoff = event["timestamp"] - self.window_seconds
        while self._window and self._window[0]["timestamp"] <= cutoff:
            old = self._window.popleft()                    # O(1)
            self._window_errors -= old["status"] >= 500

    def error_rate(self):
        return self._window_errors / len(self._window) if self._window else 0.0

    def _check_alert(self, ts):
        n, rate = len(self._window), self.error_rate()
        breached = n >= self.min_events and rate >= self.error_threshold
        if breached and not self._alerting:                 # fire once per incident
            if len(self.alerts) == self.alerts.maxlen:
                self.dropped_alerts += 1                    # oldest is discarded
            self.alerts.append({"timestamp": ts, "error_rate": rate, "window_events": n})
            self._alerting = True
        elif not breached:
            self._alerting = False

    def stats(self, endpoint):
        """Stats dict (with avg_latency_ms) or None for an unknown endpoint."""
        s = self._stats.get(endpoint)                       # O(1)
        return _with_avg(s)

    def endpoints(self):
        return list(self._stats)

    def window_size(self):
        return len(self._window)


class NaiveProcessor:
    """Baseline using only lists, for comparison. O(U + E + W) per event."""

    def __init__(self, window_seconds=60, error_threshold=0.5,
                 min_events=5, queue_size=100):
        self.window_seconds = window_seconds
        self.error_threshold = error_threshold
        self.min_events = min_events
        self._seen = []                  # list -> O(U) membership
        self._stats = []                 # list of [endpoint, stats] -> O(E) lookup
        self._window = []                # list -> O(W) pop(0)
        self._last_ts = None
        self._alerting = False
        self.alerts = []

    def process(self, event):
        validate_event(event)
        if self._last_ts is not None and event["timestamp"] < self._last_ts:
            raise ValueError("out-of-order timestamp")
        if event["id"] in self._seen:                       # O(U)
            return "duplicate"
        self._seen.append(event["id"])
        self._last_ts = event["timestamp"]
        for name, s in self._stats:                         # O(E)
            if name == event["endpoint"]:
                _update_stats(s, event)
                break
        else:
            s = _new_stats()
            _update_stats(s, event)
            self._stats.append([event["endpoint"], s])
        self._window.append(event)
        cutoff = event["timestamp"] - self.window_seconds
        while self._window and self._window[0]["timestamp"] <= cutoff:
            self._window.pop(0)                             # O(W)
        n = len(self._window)
        errors = sum(e["status"] >= 500 for e in self._window)  # O(W) recount
        rate = errors / n
        breached = n >= self.min_events and rate >= self.error_threshold
        if breached and not self._alerting:
            self.alerts.append({"timestamp": event["timestamp"],
                                "error_rate": rate, "window_events": n})
            self._alerting = True
        elif not breached:
            self._alerting = False
        return "ok"

    def stats(self, endpoint):
        for name, s in self._stats:
            if name == endpoint:
                return _with_avg(s)
        return None

    def endpoints(self):
        return [name for name, _ in self._stats]

    def error_rate(self):
        n = len(self._window)
        return sum(e["status"] >= 500 for e in self._window) / n if n else 0.0

    def window_size(self):
        return len(self._window)


def _with_avg(s):
    if s is None:
        return None
    out = dict(s)
    out["avg_latency_ms"] = s["total_latency_ms"] / s["count"] if s["count"] else 0.0
    return out
