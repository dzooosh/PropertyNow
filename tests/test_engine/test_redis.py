import unittest
from unittest.mock import patch
from engine.redis import LRUCache


class TestLRUCache(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Create an instance of LRUCache for testing
        """
        cls.cache = LRUCache()

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

    def test_delete_existing_key(self):
        """
        Test deleting an existing key
        """
        self.cache.put("key1", "value1")
        self.cache.delete("key1")
        self.assertIsNone(self.cache.get("key1"))

    def test_delete_nonexistent_key(self):
        """
        Test deleting a nonexistent key
        """
        self.cache.delete("nonexistent_key")
        self.assertIsNone(self.cache.get("nonexistent_key"))

    def test_update_existing_key(self):
        """
        Test updating an existing key
        """
        self.cache.put("key1", "value1")
        self.cache.update("key1", "new_value")
        self.assertEqual(self.cache.get("key1"), "new_value")

    def test_update_nonexistent_key(self):
        """
        Test updating a nonexistent key
        """
        self.cache.update("nonexistent_key", "value1")
        self.assertEqual(self.cache.get("nonexistent_key"), "value1")

if __name__ == "__main__":
    unittest.main()
