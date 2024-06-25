#!/usr/bin/env python3
"""Module for Last-In First-Out caching"""
from base_caching import BaseCaching
from collections import OrderedDict


class LIFOCache(BaseCaching):
    """Class object for storing and retrieving items with LIFO removal"""
    def __init__(self):
        """Initialise the caching system class"""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Puts/Adds an item in the cache"""
        if key is None or item is None:
            return
        if key not in self.cache_data:
            if len(self.cache_data) + 1 > BaseCaching.MAX_ITEMS:
                finalKey, _ = self.cache_data.popitem(True)
                print("DISCARD:", finalKey)
        self.cache_data[key] = item
        self.cache_data.move_to_end(key, last=True)

    def get(self, key):
        """Gets/Retrieves an item from the cache using a specific key"""
        return self.cache_data.get(key, None)
