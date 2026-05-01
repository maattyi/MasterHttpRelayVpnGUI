import unittest
import time
from src.proxy_server import ResponseCache


class TestResponseCache(unittest.TestCase):
    def setUp(self):
        # Create a small cache for easier testing (1 MB max size)
        self.cache = ResponseCache(max_mb=1)

    def test_initial_state(self):
        self.assertEqual(self.cache._size, 0)
        self.assertEqual(self.cache.hits, 0)
        self.assertEqual(self.cache.misses, 0)
        self.assertEqual(self.cache._max, 1 * 1024 * 1024)

    def test_cache_miss_and_hit(self):
        url = "http://example.com/test.js"
        response = b"console.log('test');"

        # Initial miss
        self.assertIsNone(self.cache.get(url))
        self.assertEqual(self.cache.misses, 1)

        # Put in cache
        self.cache.put(url, response, ttl=60)
        self.assertEqual(self.cache._size, len(response))

        # Cache hit
        cached_response = self.cache.get(url)
        self.assertEqual(cached_response, response)
        self.assertEqual(self.cache.hits, 1)

    def test_expiration_eviction(self):
        url = "http://example.com/expired.css"
        response = b"body { background: red; }"

        # Put with TTL of -1 (already expired)
        self.cache.put(url, response, ttl=-1)
        self.assertEqual(self.cache._size, len(response))

        # Should be evicted during get
        self.assertIsNone(self.cache.get(url))
        self.assertEqual(self.cache.misses, 1)
        self.assertEqual(self.cache._size, 0)
        self.assertNotIn(url, self.cache._store)

    def test_cache_eviction_when_full(self):
        # max_size is 1MB = 1048576 bytes
        # max // 4 is 262144 bytes
        # Let's put 4 items of ~200KB each (under the 1/4 max limit individually)
        chunk = b"A" * 200000

        self.cache.put("url1", chunk, ttl=60)
        self.cache.put("url2", chunk, ttl=60)
        self.cache.put("url3", chunk, ttl=60)
        self.cache.put("url4", chunk, ttl=60)

        self.assertEqual(self.cache._size, 800000)
        self.assertEqual(len(self.cache._store), 4)

        # Put a 5th item to exceed 1MB total size
        # 800000 + 250000 = 1050000 > 1048576 (1MB)
        chunk5 = b"B" * 250000
        self.cache.put("url5", chunk5, ttl=60)

        # It should have evicted url1
        self.assertNotIn("url1", self.cache._store)
        self.assertIn("url2", self.cache._store)
        self.assertIn("url3", self.cache._store)
        self.assertIn("url4", self.cache._store)
        self.assertIn("url5", self.cache._store)
        self.assertEqual(self.cache._size, 850000)

    def test_cache_replacement(self):
        url = "http://example.com/replace.js"
        response1 = b"12345"
        response2 = b"123"

        self.cache.put(url, response1, ttl=60)
        self.assertEqual(self.cache._size, 5)

        # Replace with smaller response
        self.cache.put(url, response2, ttl=60)
        self.assertEqual(self.cache._size, 3)
        self.assertEqual(self.cache.get(url), response2)

    def test_limits_rejection(self):
        url = "http://example.com/reject.js"

        # Test empty payload rejection
        self.cache.put(url, b"", ttl=60)
        self.assertEqual(self.cache._size, 0)
        self.assertNotIn(url, self.cache._store)

        # Test large payload rejection (> 25% of max)
        # 1MB / 4 = 262144 bytes
        large_response = b"C" * 262145
        self.cache.put(url, large_response, ttl=60)
        self.assertEqual(self.cache._size, 0)
        self.assertNotIn(url, self.cache._store)

    def test_parse_ttl(self):
        # Test non-200 responses
        non_200 = b"HTTP/1.1 404 Not Found\r\n\r\n"
        self.assertEqual(ResponseCache.parse_ttl(non_200, "http://ex.com"), 0)

        # Test no-store
        no_store = b"HTTP/1.1 200 OK\r\nCache-Control: no-store\r\n\r\n"
        self.assertEqual(ResponseCache.parse_ttl(no_store, "http://ex.com"), 0)

        # Test explicit max-age
        max_age = b"HTTP/1.1 200 OK\r\nCache-Control: max-age=120\r\n\r\n"
        self.assertEqual(ResponseCache.parse_ttl(max_age, "http://ex.com"), 120)

        # Test heuristic by extension (static asset)
        ext = b"HTTP/1.1 200 OK\r\n\r\n"
        self.assertEqual(ResponseCache.parse_ttl(ext, "http://ex.com/style.css"), 3600)
        self.assertEqual(ResponseCache.parse_ttl(ext, "http://ex.com/img.png?v=1"), 3600)

        # Test heuristic by Content-Type: image/font
        ct_img = b"HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n\r\n"
        self.assertEqual(ResponseCache.parse_ttl(ct_img, "http://ex.com/data"), 3600)

        # Test heuristic by Content-Type: css/js
        ct_css = b"HTTP/1.1 200 OK\r\nContent-Type: text/css; charset=utf-8\r\n\r\n"
        self.assertEqual(ResponseCache.parse_ttl(ct_css, "http://ex.com/data"), 1800)

        # Test dynamic content (html/json) default to 0
        ct_html = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        self.assertEqual(ResponseCache.parse_ttl(ct_html, "http://ex.com/data"), 0)

        # Test unhandled content type
        ct_other = b"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\n\r\n"
        self.assertEqual(ResponseCache.parse_ttl(ct_other, "http://ex.com/data"), 0)

        # Test missing headers completely
        missing_hdrs = b"HTTP/1.1 200 OK"
        self.assertEqual(ResponseCache.parse_ttl(missing_hdrs, "http://ex.com"), 0)


if __name__ == "__main__":
    unittest.main()
