#!/usr/bin/env python3
"""Module for Least Frequently Used caching"""
from base_caching import BaseCaching
from collections import OrderedDict


class LFUCache(BaseCaching):
    """Class object for storing and retrieving items with LFU removal"""
    def __init__(self):
        """Initialise the caching system class"""
        super().__init__()
        self.cache_data = OrderedDict()
        self.freqTracker = []

    def freqUpdate(self, mruKey):
        """Updates the items in the cache based on the most recently used"""
        maxPos = []
        mruFreq = 0
        mruPos = 0
        insertPos = 0
        for idx, freqTrack in enumerate(self.freqTracker):
            if freqTrack[0] == mruKey:
                mruFreq = freqTrack[1] + 1
                mruPos = idx
                break
            elif len(maxPos) == 0:
                maxPos.append(idx)
            elif freqTrack[1] < self.freqTracker[maxPos[-1]][1]:
                maxPos.append(idx)
        maxPos.reverse()
        for pos in maxPos:
            if self.freqTracker[pos][1] > mruFreq:
                break
            insertPos = pos
        self.freqTracker.pop(mruPos)
        self.freqTracker.insert(insertPos, [mruKey, mruFreq])

    def put(self, key, item):
        """Puts/Adds an item in the cache"""
        if key is None or item is None:
            return
        if key not in self.cache_data:
            if len(self.cache_data) + 1 > BaseCaching.MAX_ITEMS:
                lfuKey, _ = self.freqTracker[-1]
                self.cache_data.pop(lfuKey)
                self.freqTracker.pop()
                print("DISCARD:", lfuKey)
            self.cache_data[key] = item
            insertIdx = len(self.freqTracker)
            for idx, freqTrack in enumerate(self.freqTracker):
                if freqTrack[1] == 0:
                    insertIdx = idx
                    break
            self.freqTracker.insert(insertIdx, [key, 0])
        else:
            self.cache_data[key] = item
            self.freqUpdate(key)

    def get(self, key):
        """Gets/Retrieves an item from the cache using a specific key"""
        if key is not None and key in self.cache_data:
            self.freqUpdate(key)
        return self.cache_data.get(key, None)
