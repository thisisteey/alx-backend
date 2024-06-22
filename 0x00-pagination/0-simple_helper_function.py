#!/usr/bin/env python3
"""Module for pagination helper function index_range"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Gets & returns the idx range for paginaton based on page & page size"""
    startIdx = (page - 1) * page_size
    endIdx = startIdx + page_size
    return (startIdx, endIdx)
