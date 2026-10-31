"""Split rule - specification for splitting data into separate sheets."""
from __future__ import annotations

from typing import Dict, Optional

SplitRule = Dict[str, object]
"""
Rule for splitting data into separate sheets.

Key           | Type                    | Description
--------------|-------------------------|------------------------------------------
by_column     | str                     # Column name to split on
sheet_name_prefix | str                 # Prefix for generated sheet names (e.g., "Dept_")
include_header| bool                    # Whether each sheet keeps the header row
"""


def create_split_rule(
    by_column: str,
    sheet_name_prefix: str = "Sheet_",
    include_header: bool = True,
) -> SplitRule:
    """Create a new SplitRule dict."""
    return {
        "by_column": by_column,
        "sheet_name_prefix": sheet_name_prefix,
        "include_header": include_header,
    }