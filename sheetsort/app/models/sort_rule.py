"""Sort rule - specification for ordering the DataFrame."""
from __future__ import annotations

from typing import Dict, Literal

SortRule = Dict[str, object]
"""
Rule for ordering the DataFrame.

Key           | Type                    | Description
--------------|-------------------------|------------------------------------------
column_name   | str                     # Name of column to sort by
order         | Literal['asc', 'desc']  # Ascending or descending
custom_order  | Optional[List[str]]   # e.g., ['CSE', 'IT', 'ECE', 'Mechanical']
priority      | int                     # 0 = primary, 1 = secondary, etc.
"""


def create_sort_rule(
    column_name: str,
    order: Literal['asc', 'desc'] = 'asc',
    custom_order: Optional[List[str]] = None,
    priority: int = 0,
) -> SortRule:
    """Create a new SortRule dict."""
    return {
        "column_name": column_name,
        "order": order,
        "custom_order": custom_order or [],
        "priority": priority,
    }