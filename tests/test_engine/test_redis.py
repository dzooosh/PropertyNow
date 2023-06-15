import unittest
from unittest.mock import patch
from engine import redisCache


class TestLRUCache(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Create an instance of LRUCache for testing
        """
        cls.cache = redisCache

    @classmethod
    def tearDownClass(cls):
        """
        flush the redis client
        """
        cls.cache.flush_database()

    def setUp(self):
        """
        Clear the cache before each test
        """
        self.cache.flush_database()

    def test_put(self):
        self.cache.put("key1", "value1")
        self.assertEqual(self.cache.get("key1"), "value1")

    def test_put_eviction(self):
        """
        Test eviction of the cache system
        """
        for i in range(self.cache.MAX_ITEMS):
            self.cache.put(f"key{i}", f"value{i}")
        self.cache.put("new_key", "new_value")
        self.assertIsNone(self.cache.get("key0"))

    def test_get_existing_key(self):
        """
        Test retrieving an existing key
        """
        self.cache.put("key1", "value1")
        value = self.cache.get("key1")
        self.assertEqual(value, "value1")

    def test_get_nonexistent_key(self):
        """
        Test retrieving a nonexistent key
        """
        value = self.cache.get("nonexistent_key")
        self.assertIsNone(value)


if __name__ == "__main__":
    unittest.main()
