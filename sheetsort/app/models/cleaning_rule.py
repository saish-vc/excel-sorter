"""Cleaning rule - specification for a single cleaning operation."""
from __future__ import annotations

from typing import Dict, List, Optional, Literal

CleaningOperation = Literal[
    'trim_spaces',
    'remove_empty_rows',
    'remove_empty_cols',
    'standardize_headers',
    'date_to_ddmmyyyy',
    'normalize_phone',
    'validate_email',
    'flag_invalid',
]

CleaningRule = Dict[str, object]
"""
Rule describing a single cleaning step.

Key           | Type                    | Description
--------------|-------------------------|------------------------------------------
operation     | CleaningOperation       # What to do
enabled       | bool                    # User toggle on/off
target_columns| Optional[List[str]]     # Columns to apply to (None = all)
"""


def create_cleaning_rule(
    operation: CleaningOperation,
    enabled: bool = True,
    target_columns: Optional[List[str]] = None,
) -> CleaningRule:
    """Create a new CleaningRule dict."""
    return {
        "operation": operation,
        "enabled": enabled,
        "target_columns": target_columns,
    }