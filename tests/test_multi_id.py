import unittest
from unittest.mock import patch
import time
import sys
import os

# Add the project root to sys.path to import core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.multi_id import _Endpoint, MultiIdDispatcher

class TestEndpoint(unittest.TestCase):
    def test_initialization(self):
        ep = _Endpoint("test-id")
        self.assertEqual(ep.sid, "test-id")
        self.assertEqual(ep.ok, 0)
        self.assertEqual(ep.err, 0)
        self.assertEqual(ep.total, 0)
        self.assertEqual(ep.success_rate, 1.0)

    def test_score_basic(self):
        ep = _Endpoint("test-id")
        now = 100.0
        # Default score: success_rate * 50 = 1.0 * 50 = 50.0
        self.assertEqual(ep.score(now), 50.0)

    def test_score_with_penalties(self):
        ep = _Endpoint("test-id")
        now = 100.0
        ep.ok = 10
        ep.err = 10 # 50% success rate -> 25.0 points
        ep.latency_ms = 500.0 # penalty = 500 / 100 = 5.0
        ep.recent_failures = 1 # penalty = 1 * 20.0 = 20.0
        ep.uses = 10 # penalty = 10 * 0.25 = 2.5
        # Expected: 25.0 - 5.0 - 20.0 - 2.5 = -2.5
        self.assertEqual(ep.score(now), -2.5)

    def test_score_latency_cap(self):
        ep = _Endpoint("test-id")
        now = 100.0
        ep.latency_ms = 5000.0 # Should cap at 3000.0
        # penalty = 3000 / 100 = 30.0
        # 50.0 - 30.0 = 20.0
        self.assertEqual(ep.score(now), 20.0)

    def test_score_cooldown_penalty(self):
        ep = _Endpoint("test-id")
        now = 100.0
        ep.parked_until = 150.0
        # penalty = 80.0
        # 50.0 - 80.0 = -30.0
        self.assertEqual(ep.score(now), -30.0)

class TestMultiIdDispatcher(unittest.TestCase):
    def setUp(self):
        self.ids = ["id1", "id2", "id3"]
        self.dispatcher = MultiIdDispatcher(self.ids, fail_threshold=2, cooldown=60.0)

    def test_count(self):
        self.assertEqual(self.dispatcher.count, 3)

    @patch('time.monotonic')
    def test_next_id_round_robin(self, mock_time):
        mock_time.return_value = 100.0
        # Mock score to be constant to test pure round-robin among eligible
        with patch('core.multi_id._Endpoint.score', return_value=50.0):
            self.assertEqual(self.dispatcher.next_id(), "id1")
            self.assertEqual(self.dispatcher.next_id(), "id2")
            self.assertEqual(self.dispatcher.next_id(), "id3")
            self.assertEqual(self.dispatcher.next_id(), "id1")

    @patch('time.monotonic')
    def test_next_id_prefer_healthy(self, mock_time):
        mock_time.return_value = 100.0
        # Give id1 one failure
        self.dispatcher.report_err("id1")
        # id1 score: 50 - 20 = 30
        # id2, id3 score: 50
        # 50 - 30 = 20 > 12.0 threshold. id1 should NOT be selected.

        selected = set()
        for _ in range(6):
            selected.add(self.dispatcher.next_id())

        self.assertNotIn("id1", selected)
        self.assertIn("id2", selected)
        self.assertIn("id3", selected)

    @patch('time.monotonic')
    def test_next_id_all_parked_probing(self, mock_time):
        mock_time.return_value = 100.0
        for _ in range(2):
            self.dispatcher.report_err("id1")
            self.dispatcher.report_err("id2")
            self.dispatcher.report_err("id3")

        # All parked until 160.0
        self.assertEqual(self.dispatcher.snapshot()["endpoints_healthy"], 0)

        # Should probe the one that expires soonest
        sid = self.dispatcher.next_id()
        self.assertIn(sid, self.ids)
        ep = self.dispatcher._find(sid)
        self.assertEqual(ep.parked_until, 0.0)
        self.assertEqual(ep.recent_failures, 1)

    @patch('time.monotonic')
    def test_report_ok(self, mock_time):
        mock_time.return_value = 100.0
        self.dispatcher.report_ok("id1", latency_ms=100.0)
        ep = self.dispatcher._find("id1")
        self.assertEqual(ep.ok, 1)
        self.assertEqual(ep.latency_ms, 100.0)
        self.assertEqual(ep.recent_failures, 0)

        # Second report_ok with latency should update via moving average
        self.dispatcher.report_ok("id1", latency_ms=200.0)
        # 100 * 0.75 + 200 * 0.25 = 75 + 50 = 125
        self.assertEqual(ep.latency_ms, 125.0)

    @patch('time.monotonic')
    def test_report_err_and_parking(self, mock_time):
        mock_time.return_value = 100.0
        self.dispatcher.report_err("id1", "error")
        ep = self.dispatcher._find("id1")
        self.assertEqual(ep.err, 1)
        self.assertEqual(ep.recent_failures, 1)
        self.assertEqual(ep.parked_until, 0.0)

        # Second failure triggers parking
        self.dispatcher.report_err("id1", "error")
        self.assertEqual(ep.recent_failures, 2)
        self.assertEqual(ep.parked_until, 160.0) # 100 + 60

    @patch('time.monotonic')
    def test_health_states(self, mock_time):
        mock_time.return_value = 100.0
        self.assertEqual(self.dispatcher.health(), "good")

        # One unstable
        self.dispatcher.report_err("id1")
        self.dispatcher.report_err("id1") # parked
        self.assertEqual(self.dispatcher.health(), "unstable")

        # All down
        self.dispatcher.report_err("id2")
        self.dispatcher.report_err("id2")
        self.dispatcher.report_err("id3")
        self.dispatcher.report_err("id3")
        self.assertEqual(self.dispatcher.health(), "down")

    @patch('time.monotonic')
    def test_snapshot(self, mock_time):
        mock_time.return_value = 100.0
        self.dispatcher.report_ok("id1", latency_ms=100.0)
        self.dispatcher.report_ok("id2", latency_ms=200.0)

        snap = self.dispatcher.snapshot()
        self.assertEqual(snap["endpoints"], 3)
        self.assertEqual(snap["endpoints_healthy"], 3)
        self.assertEqual(snap["latency_ms"], 150.0)
        self.assertEqual(snap["success_rate"], 1.0)

    def test_find_non_existent(self):
        self.assertIsNone(self.dispatcher._find("non-existent"))

if __name__ == '__main__':
    unittest.main()
