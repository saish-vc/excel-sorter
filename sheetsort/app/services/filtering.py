"""Service for filtering operations on DataFrames."""
from __future__ import annotations

import pandas as pd
from typing import List, Tuple, Optional, Literal

from sheetsort.app.models.filter_rule import FilterRule, FilterCondition


def apply_filters(
    df: pd.DataFrame,
    filter_rules: List[FilterRule],
) -> Tuple[pd.DataFrame, int]:
    """Apply a list of filter rules to a DataFrame using AND/OR logic.
    
    Returns (filtered_df, row_count_reduced).
    """
    result = df.copy()
    row_reduced = 0
    
    if not filter_rules:
        return result, 0
    
    # Apply each filter rule sequentially
    combined_mask = None
    
    for i, rule in enumerate(filter_rules):
        column_name = rule.get("column_name")
        condition = rule.get("condition")
        value = rule.get("value")
        value2 = rule.get("value2")
        logic = rule.get("logic", "and")
        
        if column_name not in result.columns:
            continue
        
        col_series = result[column_name]
        
        # Build the mask for this rule
        mask = _build_filter_mask(
            col_series, condition, value, value2
        )
        
        # Combine with previous masks using the specified logic
        if combined_mask is None:
            combined_mask = mask
        elif logic == "and":
            combined_mask = combined_mask & mask
        elif logic == "or":
            combined_mask = combined_mask | mask
    
    if combined_mask is not None:
        # Apply the filter
        original_count = len(result)
        result = result[combined_mask].copy()
        row_reduced = original_count - len(result)
    
    return result, row_reduced


def _build_filter_mask(
    series: pd.Series,
    condition: FilterCondition,
    value: object,
    value2: Optional[object],
) -> pd.Series:
    """Build a boolean mask for a single filter condition."""
    mask = pd.Series(index=series.index, dtype=bool)
    
    if condition == "contains":
        # Text contains
        mask = series.astype(str).str.contains(
            str(value), case=False, na=False
        )
    
    elif condition == "exact":
        # Exact match
        mask = series == value
    
    elif condition == "gt":
        # Greater than (numeric)
        mask = pd.to_numeric(series, errors="coerce") > pd.to_numeric(value, errors="coerce")
    
    elif condition == "gte":
        # Greater than or equal
        mask = pd.to_numeric(series, errors="coerce") >= pd.to_numeric(value, errors="coerce")
    
    elif condition == "lt":
        # Less than
        mask = pd.to_numeric(series, errors="coerce") < pd.to_numeric(value, errors="coerce")
    
    elif condition == "lte":
        # Less than or equal
        mask = pd.to_numeric(series, errors="coerce") <= pd.to_numeric(value, errors="coerce")
    
    elif condition == "between":
        # Between two values (inclusive)
        if value2 is not None:
            lower = pd.to_numeric(value, errors="coerce")
            upper = pd.to_numeric(value2, errors="coerce")
            mask = (pd.to_numeric(series, errors="coerce") >= lower) & \
                   (pd.to_numeric(series, errors="coerce") <= upper)
        else:
            mask = pd.Series(index=series.index, dtype=bool)
    
    elif condition == "date_range":
        # Date range filter
        if value2 is not None:
            try:
                lower_date = pd.to_datetime(value)
                upper_date = pd.to_datetime(value2)
                series_dt = pd.to_datetime(series, errors="coerce")
                mask = (series_dt >= lower_date) & (series_dt <= upper_date)
            except (ValueError, TypeError):
                mask = pd.Series(index=series.index, dtype=bool)
        else:
            mask = pd.Series(index=series.index, dtype=bool)
    
    elif condition == "exact" and pd.api.types.is_datetime64_any_dtype(series):
        # Exact date match
        try:
            target_date = pd.to_datetime(value)
            series_dt = pd.to_datetime(series, errors="coerce")
            mask = series_dt == target_date
        except (ValueError, TypeError):
            mask = pd.Series(index=series.index, dtype=bool)
    
    else:
        # Default to exact match
        mask = series == value
    
    # Fill NaN values - mask should be False for NaN
    mask = mask.fillna(False)
    
    return mask