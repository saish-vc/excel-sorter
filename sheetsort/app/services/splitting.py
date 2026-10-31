"""Service for splitting data into separate sheets by a selected column."""
from __future__ import annotations

import pandas as pd
from typing import List, Tuple, Optional, Dict

from sheetsort.app.models.split_rule import SplitRule


def split_dataframe_by_column(
    df: pd.DataFrame,
    split_rule: SplitRule,
) -> Tuple[List[pd.DataFrame], Dict[str, int]]:
    """Split a DataFrame into multiple DataFrames by a selected column.
    
    Returns (list_of_dataframes, sheet_info_dict).
    Each DataFrame corresponds to a unique value in the split column.
    """
    result_df = df.copy()
    split_column = split_rule.get("by_column")
    include_header = split_rule.get("include_header", True)
    sheet_name_prefix = split_rule.get("sheet_name_prefix", "Sheet_")
    
    sheet_infos = {
        "total_sheets": 0,
        "total_rows": 0,
        "columns": list(result_df.columns),
    }
    
    if split_column not in result_df.columns:
        # Split column not found; return original as single sheet
        dfs = [result_df]
        sheet_infos["total_sheets"] = 1
        sheet_infos["total_rows"] = len(result_df)
        return dfs, sheet_infos
    
    # Get unique values in the split column
    # Handle NaN by filling with a placeholder
    split_col_series = result_df[split_column].fillna("__UNKNOWN__")
    unique_values = split_col_series.unique()
    
    dfs = []
    for val in unique_values:
        # Filter rows where split column equals this value
        mask = split_col_series == val
        subset = result_df[mask].copy()
        
        # Reset index
        subset = subset.reset_index(drop=True)
        
        # Excel sheet names cannot contain : \\ / ? * [ or ].
        if include_header:
            safe_val = "".join("_" if char in ':\\/?*[]' else char for char in str(val))
            sheet_name = f"{sheet_name_prefix}{safe_val}"
        else:
            sheet_name = f"{sheet_name_prefix}{sheet_infos['total_sheets'] + 1}"
        
        # Ensure sheet name is unique
        final_sheet_name = _ensure_sheet_name_unique(dfs, sheet_name)
        subset.attrs["sheet_name"] = final_sheet_name
        
        dfs.append(subset)
        sheet_infos["total_sheets"] += 1
        sheet_infos["total_rows"] += len(subset)
    
    return dfs, sheet_infos


def _ensure_sheet_name_unique(
    existing_dfs: List[pd.DataFrame],
    proposed_name: str,
) -> str:
    """Ensure a sheet name is unique among existing ones."""
    name = proposed_name[:31]  # Excel limit
    
    # Check if name already exists
    counter = 1
    base_name = name
    while any(
        df.attrs.get("sheet_name", "") == name 
        for df in existing_dfs 
        if len(df) > 0
    ):
        # Add suffix before .xlsx extension limit
        if "." in name:
            name_part, ext = name.rsplit(".", 1)
        else:
            name_part = name
            ext = ""
        proposed = f"{name_part}_{counter}"
        if len(proposed) > 31:
            # Truncate and add counter
            available = 31 - len(str(counter)) - 1
            name_part = proposed[:available]
            proposed = f"{name_part}_{counter}"
        counter += 1
        name = proposed
    
    return name
