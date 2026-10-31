"""Filter rule - specification for filtering rows."""
from __future__ import annotations

from typing import Dict, Literal, Optional

FilterCondition = Literal['contains', 'exact', 'gt', 'gte', 'lt', 'lte', 'between', 'date_range']

FilterRule = Dict[str, object]
"""
Rule for filtering rows.

Key           | Type                    | Description
--------------|-------------------------|------------------------------------------
column_name   | str                     # Column to filter on
condition     | FilterCondition         # Type of comparison
value         | object                  # Depends on condition (e.g., number, date string, text)
value2        | Optional[object]      # For 'between' / 'date_range'
logic         | Literal['and', 'or']  # How this combines with other filters
"""


def create_filter_rule(
    column_name: str,
    condition: FilterCondition,
    value: object,
    value2: Optional[object] = None,
    logic: Literal['and', 'or'] = 'and',
) -> FilterRule:
    """Create a new FilterRule dict."""
    return {
        "column_name": column_name,
        "condition": condition,
        "value": value,
        "value2": value2,
        "logic": logic,
    }