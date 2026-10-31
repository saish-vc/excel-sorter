"""Service for duplicate detection and removal."""
from __future__ import annotations

import pandas as pd
from typing import List, Literal, Optional, Tuple

from sheetsort.app.models.sort_rule import SortRule


def detect_and_remove_duplicates(
    df: pd.DataFrame,
    keep: Literal['first', 'last'] = 'first',
    subset: Optional[List[str]] = None,
    detect_near_duplicates: bool = False,
    near_duplicates_subset: Optional[List[str]] = None,
    near_duplicates_threshold: float = 0.9,
) -> Tuple[pd.DataFrame, int, int, List[dict]]:
    """Detect and remove exact and/or near-duplicate rows.
    
    Returns (deduped_df, exact_duplicates_removed, near_duplicates_removed, duplicate_details).
    """
    result = df.copy()
    exact_removed = 0
    near_duplicates_removed = 0
    duplicate_details = []
    
    # Step 1: Remove exact duplicates
    before_count = len(result)
    
    if subset:
        # Only consider specified columns for duplicate detection
        subset_cols = [c for c in subset if c in result.columns]
        if subset_cols:
            duplicates_mask = result.duplicated(
                subset=subset_cols, keep=keep
            )
        else:
            duplicates_mask = result.duplicated(keep=keep)
    else:
        duplicates_mask = result.duplicated(keep=keep)
    
    exact_removed = int(duplicates_mask.sum())
    
    if exact_removed > 0:
        # Show details before removal
        duplicate_indices = result[duplicates_mask].index.tolist()
        for idx in duplicate_indices:
            row_data = result.loc[idx].to_dict()
            duplicate_details.append({
                "type": "exact",
                "index": idx,
                "row_data": row_data,
            })
        
        result = result.loc[~duplicates_mask].copy()
        
        # Record original count before removal for this step
        # exact_removed already counted
    
    # Step 2: Near-duplicate detection (optional)
    if detect_near_duplicates and near_duplicates_subset:
        near_removed, near_details = _detect_near_duplicates(
            result,
            near_duplicates_subset,
            near_duplicates_threshold,
        )
        near_duplicates_removed = near_removed
        duplicate_details.extend(near_details)
        
        if near_removed > 0:
            # Filter out near-duplicate rows
            mask = pd.Series(False, index=result.index)
            for idx, to_remove in near_details:
                if to_remove:
                    mask.loc[idx] = True
            result = result[~mask].copy()
    
    return result, exact_removed, near_duplicates_removed, duplicate_details


def _detect_near_duplicates(
    df: pd.DataFrame,
    subset: List[str],
    threshold: float,
) -> Tuple[int, List[Tuple[int, bool]]]:
    """Detect near-duplicates based on selected columns similarity.
    
    Returns (count_of_rows_to_remove, list of (index, should_remove) tuples).
    """
    import numpy as np
    
    result = df.copy()
    count_removed = 0
    details = []
    
    if len(df) < 2:
        return 0, []
    
    # Get the subset columns
    subset_cols = [c for c in subset if c in result.columns]
    if not subset_cols:
        return 0, []
    
    # Work with selected columns only
    work_df = result[subset_cols].copy()
    
    # Encode categorical data for comparison
    # Simple approach: convert to strings and compare
    for col in subset_cols:
        work_df[col] = work_df[col].astype(str)
    
    # Calculate pairwise similarity
    # For MVP, use a simple row-by-row comparison
    rows_to_remove = set()
    
    for i in range(len(work_df)):
        if i in rows_to_remove:
            continue
        for j in range(i + 1, len(work_df)):
            if j in rows_to_remove:
                continue
            
            # Calculate similarity ratio
            series_i = work_df.iloc[i]
            series_j = work_df.iloc[j]
            
            # Count matching values
            matching = 0
            total = 0
            for col in subset_cols:
                v1 = series_i[col]
                v2 = series_j[col]
                total += 1
                if v1 == v2:
                    matching += 1
            
            if total > 0 and matching / total >= threshold:
                # Mark the later row for removal
                if j not in rows_to_remove:
                    rows_to_remove.add(j)
                    count_removed += 1
                    details.append((j, True))  # j should be removed
    
    return count_removed, details
