import importlib.util
import os
import unittest


def load_cache_class():
    path = os.environ["CACHE_SUBMISSION"]
    spec = importlib.util.spec_from_file_location("cache_submission", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.TTLCache


TTLCache = load_cache_class()


class FakeClock:
    def __init__(self):
        self.now = 100.0

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


class TTLCacheTests(unittest.TestCase):
    def setUp(self):
        self.clock = FakeClock()

    def test_basic_set_get_and_default(self):
        cache = TTLCache(2, clock=self.clock)
        cache.set("a", 7)
        self.assertEqual(cache.get("a"), 7)
        self.assertEqual(cache.get("missing", "fallback"), "fallback")

    def test_expiration_uses_injected_clock(self):
        cache = TTLCache(2, default_ttl=5, clock=self.clock)
        cache.set("a", 1)
        self.clock.advance(5)
        self.assertIsNone(cache.get("a"))

    def test_non_positive_ttl_expires_immediately(self):
        cache = TTLCache(2, clock=self.clock)
        cache.set("zero", 1, ttl=0)
        cache.set("negative", 2, ttl=-1)
        self.assertEqual(len(cache), 0)

    def test_len_contains_and_prune_ignore_expired(self):
        cache = TTLCache(3, clock=self.clock)
        cache.set("short", 1, ttl=1)
        cache.set("long", 2, ttl=10)
        self.clock.advance(2)
        self.assertNotIn("short", cache)
        self.assertIn("long", cache)
        self.assertEqual(len(cache), 1)
        self.assertEqual(cache.prune_expired(), 0)

    def test_prune_returns_number_removed(self):
        cache = TTLCache(3, clock=self.clock)
        cache.set("a", 1, ttl=1)
        cache.set("b", 2, ttl=2)
        cache.set("c", 3, ttl=10)
        self.clock.advance(3)
        self.assertEqual(cache.prune_expired(), 2)
        self.assertEqual(len(cache), 1)

    def test_capacity_evicts_least_recently_used(self):
        cache = TTLCache(2, clock=self.clock)
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)
        self.assertIsNone(cache.get("a"))
        self.assertEqual(cache.get("b"), 2)
        self.assertEqual(cache.get("c"), 3)

    def test_get_refreshes_recency(self):
        cache = TTLCache(2, clock=self.clock)
        cache.set("a", 1)
        cache.set("b", 2)
        self.assertEqual(cache.get("a"), 1)
        cache.set("c", 3)
        self.assertIn("a", cache)
        self.assertNotIn("b", cache)

    def test_expired_entries_are_removed_before_live_eviction(self):
        cache = TTLCache(2, clock=self.clock)
        cache.set("expired", 1, ttl=1)
        cache.set("live", 2, ttl=20)
        self.clock.advance(2)
        cache.set("new", 3, ttl=20)
        self.assertIn("live", cache)
        self.assertIn("new", cache)
        self.assertEqual(len(cache), 2)

    def test_overwrite_replaces_expiry_and_refreshes_recency(self):
        cache = TTLCache(2, clock=self.clock)
        cache.set("a", 1, ttl=1)
        cache.set("b", 2, ttl=20)
        cache.set("a", 3, ttl=20)
        self.clock.advance(2)
        self.assertEqual(cache.get("a"), 3)
        cache.set("c", 4)
        self.assertNotIn("b", cache)

    def test_invalid_capacity_is_rejected(self):
        for value in (0, -1, 1.5, True):
            with self.assertRaises(ValueError):
                TTLCache(value, clock=self.clock)

    def test_clear(self):
        cache = TTLCache(2, clock=self.clock)
        cache.set("a", 1)
        cache.clear()
        self.assertEqual(len(cache), 0)


if __name__ == "__main__":
    unittest.main()
