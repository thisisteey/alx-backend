#!/usr/bin/env python3
"""Deletion-resilient hypermedia pagination"""
import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names"""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initialize the server instance"""
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset from the csv file"""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0"""
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """Gets info about a page from a specific index with a given size"""
        idData = self.indexed_dataset()
        assert index is not None and index >= 0 and index <= max(idData.keys())
        data = []
        dataCount = 0
        next_index = None
        startIdx = index if index else 0
        for x, element in idData.items():
            if x >= startIdx and dataCount < page_size:
                data.append(element)
                dataCount += 1
                continue
            if dataCount == page_size:
                next_index = x
                break
        pageHyperMediaInfo = {
            "index": index,
            "next_index": next_index,
            "page_size": len(data),
            "data": data
        }
        return pageHyperMediaInfo
