"""Service for sorting operations on DataFrames."""
from __future__ import annotations

import pandas as pd
from typing import List, Tuple, Optional

from sheetsort.app.models.sort_rule import SortRule


def apply_sorting(
    df: pd.DataFrame,
    sort_rules: List[SortRule],
) -> Tuple[pd.DataFrame, bool]:
    """Apply multi-column sorting rules to a DataFrame.

    Returns (sorted_df, had_sorting).
    If no sort rules are provided, the DataFrame is returned unchanged.
    """
    result = df.copy()
    
    if not sort_rules:
        return result, False
    
    # Sort by priority order
    sorted_rules = sorted(sort_rules, key=lambda r: r.get("priority", 0))
    
    for rule in sorted_rules:
        column_name = rule.get("column_name")
        order = rule.get("order", "asc")
        custom_order = rule.get("custom_order")
        
        if column_name not in result.columns:
            # Column not found; skip this rule
            continue
        
        # Determine sort order
        ascending = order == "asc"
        
        if custom_order:
            # Custom order sorting using Categorical dtype
            try:
                # Convert column to ordered Categorical for proper sorting
                result[column_name] = pd.Categorical(
                    result[column_name],
                    categories=custom_order,
                    ordered=True
                )
                result = result.sort_values(
                    by=column_name,
                    ascending=ascending,
                    inplace=False,
                )
            except Exception:
                # Fallback to default sorting
                result = result.sort_values(
                    by=column_name,
                    ascending=ascending,
                    inplace=False,
                )
        else:
            result = result.sort_values(
                by=column_name,
                ascending=ascending,
                inplace=False,
            )
    
    return result, True