import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from processor import ApiProcessor, NaiveProcessor  # noqa: E402


def ev(i, ts, status=200, ep="/a", lat=10.0):
    return {"id": f"id{i}", "endpoint": ep, "status": status,
            "latency_ms": lat, "timestamp": ts}


class Contract:
    """Run every test against both the chosen and the baseline implementation."""

    def make(self, **kw):
        return self.cls(**kw)

    def test_stats_aggregation(self):
        p = self.make()
        p.process(ev(1, 1, 200, "/x", 10))
        p.process(ev(2, 2, 500, "/x", 30))
        s = p.stats("/x")
        self.assertEqual((s["count"], s["errors"], s["max_latency_ms"]), (2, 1, 30))
        self.assertAlmostEqual(s["avg_latency_ms"], 20.0)

    def test_duplicate_ignored(self):
        p = self.make()
        self.assertEqual(p.process(ev(1, 1)), "ok")
        self.assertEqual(p.process(ev(1, 2)), "duplicate")
        self.assertEqual(p.stats("/a")["count"], 1)

    def test_unknown_endpoint_is_none(self):
        self.assertIsNone(self.make().stats("/missing"))

    def test_empty_processor(self):
        p = self.make()
        self.assertEqual(p.error_rate(), 0.0)
        self.assertEqual(p.endpoints(), [])

    def test_invalid_events_rejected(self):
        p = self.make()
        bad = [ev(1, 1, status=99), ev(2, 1, status=600), ev(3, 1, lat=-1),
               {"id": "x"}, "not a dict", ev(4, 1, ep="")]
        for b in bad:
            with self.assertRaises(ValueError, msg=str(b)):
                p.process(b)

    def test_status_boundaries_accepted(self):
        p = self.make()
        for i, st in enumerate((100, 499, 500, 599)):
            self.assertEqual(p.process(ev(i, i, st)), "ok")
        self.assertAlmostEqual(p.error_rate(), 0.5)

    def test_out_of_order_rejected(self):
        p = self.make()
        p.process(ev(1, 10))
        with self.assertRaises(ValueError):
            p.process(ev(2, 5))

    def test_window_boundary_exact_age_evicted(self):
        p = self.make(window_seconds=10)
        p.process(ev(1, 0, 500))
        p.process(ev(2, 9.99))
        self.assertEqual(p.window_size(), 2)
        p.process(ev(3, 10))             # first event is exactly 10s old -> evicted
        self.assertEqual(p.window_size(), 2)
        self.assertEqual(p.error_rate(), 0.0)

    def test_alert_fires_once_and_rearms(self):
        p = self.make(window_seconds=5, error_threshold=0.5, min_events=2)
        p.process(ev(1, 0, 500)); p.process(ev(2, 1, 500))
        p.process(ev(3, 2, 500))                         # still breached: no new alert
        self.assertEqual(len(p.alerts), 1)
        for i in range(4, 14):
            p.process(ev(i, i, 200))                     # recover
        p.process(ev(100, 100, 500)); p.process(ev(101, 101, 500))
        self.assertEqual(len(p.alerts), 2)

    def test_no_alert_below_min_events(self):
        p = self.make(min_events=5)
        for i in range(4):
            p.process(ev(i, i, 500))
        self.assertEqual(len(p.alerts), 0)
        p.process(ev(4, 4, 500))
        self.assertEqual(len(p.alerts), 1)


class TestApiProcessor(Contract, unittest.TestCase):
    cls = ApiProcessor

    def test_invalid_config(self):
        for kw in ({"window_seconds": 0}, {"error_threshold": 0},
                   {"error_threshold": 1.5}, {"queue_size": 0}):
            with self.assertRaises(ValueError):
                ApiProcessor(**kw)

    def test_alert_queue_overflow_drops_oldest(self):
        p = ApiProcessor(window_seconds=1, error_threshold=0.5, min_events=1, queue_size=2)
        t = 0
        for i in range(5):                               # 5 separate incidents
            p.process(ev(f"e{i}", t, 500)); t += 10
            p.process(ev(f"o{i}", t, 200)); t += 10
        self.assertEqual(len(p.alerts), 2)
        self.assertEqual(p.dropped_alerts, 3)


class TestNaiveProcessor(Contract, unittest.TestCase):
    cls = NaiveProcessor


class TestEquivalence(unittest.TestCase):
    def test_both_implementations_agree_on_sample_data(self):
        events = json.loads((ROOT / "sample_data.json").read_text())
        a, b = ApiProcessor(10, 0.5, 4), NaiveProcessor(10, 0.5, 4)
        for e in events:
            ra = rb = None
            try: ra = a.process(e)
            except ValueError: ra = "error"
            try: rb = b.process(e)
            except ValueError: rb = "error"
            self.assertEqual(ra, rb)
        self.assertEqual(a.endpoints(), b.endpoints())
        for ep in a.endpoints():
            self.assertEqual(a.stats(ep), b.stats(ep))
        self.assertEqual(list(a.alerts), b.alerts)


if __name__ == "__main__":
    unittest.main()
