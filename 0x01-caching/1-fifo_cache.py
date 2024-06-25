#!/usr/bin/env python3
"""Module for First-In First-Out caching"""
from base_caching import BaseCaching
from collections import OrderedDict


class FIFOCache(BaseCaching):
    """Class object for storing and retrieving items with FIFO removal"""
    def __init__(self):
        """Initialise the caching system class"""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Puts/Adds an item in the cache"""
        if key is None or item is None:
            return
        self.cache_data[key] = item
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            initialKey, _ = self.cache_data.popitem(False)
            print("DISCARD:", initialKey)

    def get(self, key):
        """Gets/Retrieves an item from the cache using a specific key"""
        return self.cache_data.get(key, None)
