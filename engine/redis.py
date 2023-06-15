"""
MRUCache module
"""
from os import environ
import redis
import json


class LRUCache:
    """
    A caching system that uses the Least Recently Used (LRU)
    algorithm to add and remove values.

    Methods:
    -------
    put(key: Any, value: Any) -> None:
        Adds a key-value pair to the cache. If the cache is at capacity,
        removes the Least recently used key-value pair.

    get(key: Any) -> Any:
        Returns the value associated with the given key.
        If the key doesn't exist, returns None.

    delete(key: Any) -> None:
        Removes the key-value pair from the cache, if it exists.

    update(key: Any, value: Any) -> None:
        Updates the value associated with the given key in the cache.
        If the key doesn't exist, adds the key-value pair to the cache.
    """

    MAX_ITEMS = 100

    def __init__(self):
        """
        Initialize `RedisClient` class
        """
        REDIS_HOST = environ.get('REDIS_HOST', 'localhost')
        REDIS_PORT = environ.get('REDIS_PORT', '6379')
        self.__cacheClient = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

    def put(self, key, value):
        """
        Adds a key-value pair to the cache. If the cache is at capacity,
        removes the least recently used key-value pair.

        Parameters:
        ----------
        key : Any
            The key to be added to the cache.
        value : Any
            The value associated with the key.

        Returns:
        -------
        None
        """
        value = json.dumps(value)
        self.__cacheClient.set(key, value)
        if self.__cacheClient.dbsize() > self.MAX_ITEMS:
            lru_key = self.__cacheClient.execute_command('LINDEX', 'LRU_KEYS', -1)
            self.__cacheClient.delete(lru_key)
            self.__cacheClient.execute_command('LREM', 'LRU_KEYS', 0, lru_key)
        self.__cacheClient.execute_command('LPUSH', 'LRU_KEYS', key)

    def get(self, key):
        """
        Returns the value associated with the given key.
        If the key doesn't exist, returns None.

        Parameters:
        ----------
        key : Any
            The key to retrieve the value for.

        Returns:
        -------
        Any
            The value associated with the key, or None if the key doesn't exist.
        """
        value = self.__cacheClient.get(key)
        if value:
            self.__cacheClient.execute_command('LREM', 'LRU_KEYS', 0, key)
            self.__cacheClient.execute_command('LPUSH', 'LRU_KEYS', key)
            value = value.decode('utf-8')
            return json.loads(value)
        else:
            return None

    def delete(self, key):
        """
        Removes the key-value pair from the cache, if it exists.

        Parameters:
        ----------
        key : Any
            The key to be removed from the cache.

        Returns:
        -------
        None
        """
        if self.__cacheClient.exists(key):
            self.__cacheClient.delete(key)
            self.__cacheClient.execute_command('LREM', 'LRU_KEYS', 0, key)

    def update(self, key, value):
        """
        Updates the value associated with the given key in the cache.
        If the key doesn't exist, adds the key-value pair to the cache.

        Parameters:
        ----------
        key : Any
            The key to be updated or added to the cache.
        value : Any
            The new value associated with the key.

        Returns:
        -------
        None
        """
        if self.__cacheClient.exists(key):
            value = json.dumps(value)
            self.__cacheClient.set(key, value)
            self.__cacheClient.execute_command('LREM', 'LRU_KEYS', 0, key)
        else:
            self.put(key, value)

    def flush_database(self):
        """
        flushes the database
        """
        self.__cacheClient.flushdb()
    