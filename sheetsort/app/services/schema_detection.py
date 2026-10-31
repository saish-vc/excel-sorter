"""Service for detecting schema: header row and column data types."""
from __future__ import annotations

import re
from typing import List, Tuple, Optional, Dict

import pandas as pd

from sheetsort.app.models.column_metadata import (
    ColumnType,
    ColumnMetadata,
    create_column_metadata,
    _normalize_name,
)


def detect_header_row(
    df: pd.DataFrame,
    suspected_row: Optional[int] = None,
) -> Tuple[int, bool]:
    """Detect the row index that contains headers.
    
    Returns (header_row_index, success).
    If suspected_row is provided, use that row; otherwise auto-detect.
    """
    max_rows_to_check = min(5, len(df) - 1)
    
    if suspected_row is not None and 0 <= suspected_row < len(df):
        row = df.iloc[suspected_row]
        # Check if the row looks like headers (contains string-like values)
        non_null_count = row.notna().sum()
        ratio = non_null_count / len(row) if len(row) > 0 else 0
        if ratio >= 0.6 and ratio > 0:
            return suspected_row, True
    
    # Auto-detect: check first 5 rows for header-like content
    for i in range(max_rows_to_check):
        row = df.iloc[i]
        non_null_count = row.notna().sum()
        ratio = non_null_count / len(row) if len(row) > 0 else 0
        
        # Heuristic: if more than 50% of non-null values are strings,
        # it's likely a header row
        if ratio > 0:
            string_ratio = sum(1 for val in row if isinstance(val, str)) / ratio
            if string_ratio >= 0.7:
                return i, True
    
    # No header detected; use row 0 as forced header
    return 0, False


def detect_column_data_types(
    df: pd.DataFrame,
    header_row: int,
) -> Tuple[List[ColumnMetadata], pd.DataFrame]:
    """Detect data types for each column after the header row.
    
    Returns (column_metadata_list, data_df_with_header_set).
    The DataFrame has its header set to the detected row.
    """
    # Set the header row and drop it from data
    data_df = df.iloc[header_row + 1:].copy()
    data_df.columns = df.iloc[header_row]
    
    # Strip column names
    data_df.columns = [
        str(col).strip() if col is not None else f"col_{i}"
        for col in data_df.columns
    ]
    
    # Remove duplicate column names
    data_df = _remove_duplicate_columns(data_df)
    
    column_metadata_list: List[ColumnMetadata] = []
    
    for i, col in enumerate(data_df.columns):
        series = data_df[col]
        
        # Determine data type
        data_type = _classify_column_type(series)
        
        # Get sample values (first 5 non-null)
        sample_values = series.dropna().head(5).tolist()
        # Convert sample values to strings for display
        sample_values = [
            str(v) if v is not None else None for v in sample_values
        ]
        
        # Normalize column name
        normalized_name = _normalize_name(str(col))
        
        # Check if this looks like a header row (we already set it)
        is_header = True
        
        metadata = create_column_metadata(
            column_name=str(col),
            column_index=i,
            data_type=data_type,
            sample_values=sample_values,
            is_header=is_header,
            normalized_name=normalized_name,
        )
        column_metadata_list.append(metadata)
    
    return column_metadata_list, data_df


def _classify_column_type(series: pd.Series) -> ColumnType:
    """Classify a pandas Series into one of the ColumnType values."""
    non_null = series.dropna()
    if len(non_null) == 0:
        return "text"
    
    sample = non_null.head(20)
    
    # Check if all values can be parsed as dates
    if _all_can_be_dates(sample):
        return "date"
    
    # Check if all values look like email addresses
    if _all_look_like_emails(sample):
        return "email"
    
    # Check if all values look like phone numbers
    if _all_look_like_phones(sample):
        return "phone"
    
    # Check if all values look like IDs (numeric, no decimal, reasonable length)
    if _all_look_like_ids(sample):
        return "id"
    
    # Default to text
    return "text"


def _all_can_be_dates(sample: pd.Series) -> bool:
    """Check if all sample values can be parsed as dates."""
    date_count = 0
    for val in sample:
        try:
            pd.to_datetime(val)
            date_count += 1
        except (ValueError, TypeError):
            pass
    return date_count / len(sample) > 0.8 if len(sample) > 0 else False


def _all_look_like_emails(sample: pd.Series) -> bool:
    """Check if all sample values look like email addresses."""
    import re
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    email_count = sum(
        1 for val in sample 
        if isinstance(val, str) and re.match(email_pattern, str(val).strip())
    )
    return email_count / len(sample) > 0.8 if len(sample) > 0 else False


def _all_look_like_phones(sample: pd.Series) -> bool:
    """Check if all sample values look like phone numbers."""
    import re
    phone_pattern = r"^\+?[1-9]\d{7,14}$"
    phone_count = sum(
        1 for val in sample 
        if isinstance(val, str) and re.match(phone_pattern, str(val).strip())
    )
    return phone_count / len(sample) > 0.8 if len(sample) > 0 else False


def _all_look_like_ids(sample: pd.Series) -> bool:
    """Check if all sample values look like IDs (numeric, no decimal)."""
    numeric_count = 0
    for val in sample:
        if isinstance(val, (int, float)):
            numeric_count += 1
        elif isinstance(val, str):
            # Remove whitespace and check if it's purely digits
            cleaned = val.strip()
            if cleaned.isdigit() and 3 <= len(cleaned) <= 20:
                numeric_count += 1
    return numeric_count / len(sample) > 0.8 if len(sample) > 0 else False


def _remove_duplicate_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Handle duplicate column names by auto-renaming."""
    cols = list(df.columns)
    seen: Dict[str, int] = {}
    new_cols = []
    
    for col in cols:
        if col in seen:
            seen[col] += 1
            new_cols.append(f"{col}_{seen[col]}")
        else:
            seen[col] = 0
            new_cols.append(col)
    
    df.columns = new_cols
    return df