"""Run the API monitor on sample_data.json.

    python main.py                 # process sample data
    python main.py --benchmark     # compare list baseline vs set/dict/deque
"""
import json
import sys
import time
from pathlib import Path

from processor import ApiProcessor, NaiveProcessor


def run_sample(path):
    events = json.loads(Path(path).read_text())
    p = ApiProcessor(window_seconds=10, error_threshold=0.5, min_events=4)
    counts = {"ok": 0, "duplicate": 0, "rejected": 0}
    for ev in events:
        try:
            counts[p.process(ev)] += 1
        except ValueError as exc:
            counts["rejected"] += 1
            print(f"  rejected {ev.get('id')}: {exc}")
    print("\nResults:", counts)
    for ep in p.endpoints():
        s = p.stats(ep)
        print(f"  {ep:<10} count={s['count']} errors={s['errors']} "
              f"avg={s['avg_latency_ms']:.1f}ms max={s['max_latency_ms']}ms")
    for a in p.alerts:
        print(f"  ALERT at t={a['timestamp']}: error rate {a['error_rate']:.0%} "
              f"over {a['window_events']} events")


def benchmark(n=5000):
    events = [{"id": f"id{i}", "endpoint": f"/api/e{i % 200}",
               "status": 500 if i % 5 == 0 else 200,
               "latency_ms": 10.0, "timestamp": float(i)} for i in range(n)]
    print(f"Benchmark: {n} events, window=2000s")
    for cls in (NaiveProcessor, ApiProcessor):
        p = cls(window_seconds=2000)
        t = time.perf_counter()
        for ev in events:
            p.process(ev)
        print(f"  {cls.__name__:<15}{(time.perf_counter() - t) * 1000:9.1f} ms")


if __name__ == "__main__":
    if "--benchmark" in sys.argv:
        benchmark()
    else:
        run_sample(Path(__file__).with_name("sample_data.json"))
