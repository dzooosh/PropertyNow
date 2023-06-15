"""
initialize the models package
"""
from engine.db import Storage
from engine.redis import LRUCache

storage = Storage()
redisCache = LRUCache()