#!/usr/bin/env python3
"""Module for pagination of a dataset of baby names"""
import csv
import math
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Gets & returns the idx range for paginaton based on page & page size"""
    startIdx = (page - 1) * page_size
    endIdx = startIdx + page_size
    return (startIdx, endIdx)


class Server:
    """Server class to paginate a database of popular baby names"""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initialize the server instance"""
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset from the csv file"""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Gets and returns a specific page of baby names"""
        assert type(page) == int and type(page_size) == int
        assert page > 0 and page_size > 0
        startIdx, endIdx = index_range(page, page_size)
        dataSets = self.dataset()
        if startIdx > len(dataSets):
            return []
        return dataSets[startIdx:endIdx]
