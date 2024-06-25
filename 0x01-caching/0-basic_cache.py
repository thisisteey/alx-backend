#!/usr/bin/env python3
"""Module for basic caching implementation"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """Class that represents object for storing and retrieving items"""
    def __init__(self):
        """Initialise the caching system class"""
        super().__init__()
        self.cache_data = {}

    def put(self, key, item):
        """Puts/Adds an item in the cache"""
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """Gets/Retrieves an item from the cache using a specific key"""
        return self.cache_data.get(key, None)
