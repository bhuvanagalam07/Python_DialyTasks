# Data Structures Day 1 - API Monitoring Processor

A small processor for a stream of API call events. It ignores duplicates, keeps per-endpoint
stats, tracks the error rate over a sliding time window, and queues alerts.
Each job is done with a **chosen** structure and compared with a **list baseline**.

## Files
| File | Purpose |
|---|---|
| `processor.py` | `ApiProcessor` (set/dict/deque) and `NaiveProcessor` (lists) |
| `main.py` | Runs the sample data, or `--benchmark` |
| `sample_data.json` | 13 events incl. a duplicate, bad status, negative latency, out-of-order event |
| `tests/test_processor.py` | 23 unit tests (every contract test runs on both implementations) |

## How to run
Requires Python 3.8+. No packages to install.
```
python main.py                                  # process sample_data.json
python main.py --benchmark                      # list vs set/dict/deque timing
python -m unittest discover -s tests -v         # run tests
```
Expected `python main.py` output:
```
  rejected e8: invalid status: 999
  rejected e9: latency_ms must be >= 0
  rejected e10: out-of-order timestamp

Results: {'ok': 9, 'duplicate': 1, 'rejected': 3}
  /users     count=3 errors=0 avg=36.8ms max=42.5ms
  /orders    count=2 errors=0 avg=77.5ms max=80.0ms
  /payments  count=4 errors=4 avg=417.5ms max=520.0ms
  ALERT at t=5: error rate 50% over 6 events
```

## Decisions and complexity
U = unique ids seen, E = distinct endpoints, W = events in window, Q = alert queue size.

| Job | Baseline (list) | Chosen | Why |
|---|---|---|---|
| Duplicate check | `in list` - O(U) | `set` - **O(1)** avg | only membership is needed |
| Stats per endpoint | scan list - O(E) | `dict` - **O(1)** avg | lookup by key |
| Sliding window | `list.pop(0)` - O(W) | `deque.popleft()` - **O(1)** | FIFO: add right, evict left |
| Error count in window | recount - O(W) | running counter - **O(1)** | updated on add/evict |
| Alert buffer | list | `deque(maxlen=Q)` - **O(1)** | bounded FIFO, oldest dropped and counted |

Per event: baseline O(U + E + W), chosen **amortised O(1)** (each event enters and leaves the window once).
Space is O(U + E + W + Q) for both; the set/dict use more memory per item than a list because
hash tables keep spare slots. That is the trade: more memory for much faster lookups.

Measured (`--benchmark`, 5,000 events, one machine): baseline ~350 ms vs chosen ~9 ms (~40x).
The gap widens as the data grows because the baseline is quadratic overall.

## Rules implemented
- Error = status >= 500. Valid status 100-599, latency >= 0, all fields present, else `ValueError`.
- Window keeps events with `timestamp > now - window_seconds` (exactly window-old is evicted).
- An alert fires when the window has >= `min_events` and error rate >= threshold, once per incident; it re-arms after recovery.

## Test evidence
- Success: stats, error rate, alert fire/re-arm, both implementations agree on `sample_data.json`.
- Negative: duplicates, invalid status/latency/fields/non-dict, out-of-order timestamp, unknown endpoint, bad config.
- Boundary: status 100/499/500/599, event exactly at window edge, `min_events` minus one, alert queue overflow, empty processor.

## Known limitations
- Seen ids are never expired, so memory grows with U (production: TTL/LRU).
- Timestamps must be non-decreasing; late events are rejected, not reordered.
- Not thread-safe (use a lock or single consumer).
- Average-case O(1) for set/dict; no percentiles (p95/p99).
