"""Service for data cleaning operations."""
from __future__ import annotations

import pandas as pd
import re
from typing import List, Tuple, Optional, Set

from sheetsort.app.models.column_metadata import _normalize_name
from sheetsort.app.models.cleaning_rule import (
    CleaningRule,
    CleaningOperation,
    create_cleaning_rule,
)
from sheetsort.app.utils.config import DEFAULT_DATE_FORMAT

# Handle duplicate column names after standardization
def _remove_duplicate_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate column names."""
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


def apply_cleaning_rules(
    df: pd.DataFrame,
    cleaning_rules: List[CleaningRule],
) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """Apply a list of cleaning rules to a DataFrame.
    
    Returns (cleaned_df, operation_counts_dict).
    The counts dict tracks how many operations were applied per category.
    """
    counts = {
        "trim_spaces": 0,
        "remove_empty": 0,
        "standardize_headers": 0,
        "date_conversion": 0,
        "phone_normalization": 0,
        "email_validation": 0,
        "invalid_flagged": 0,
    }
    
    result_df = df.copy()
    
    for rule in cleaning_rules:
        if not rule.get("enabled", True):
            continue
        
        operation = rule["operation"]
        target_cols = rule.get("target_columns")
        
        if operation == "trim_spaces":
            result_df = _trim_spaces(result_df)
            counts["trim_spaces"] += 1
        
        elif operation == "remove_empty_rows":
            result_df = _remove_empty_rows(result_df)
            counts["remove_empty"] += 1
        
        elif operation == "remove_empty_cols":
            result_df = _remove_empty_cols(result_df)
            counts["remove_empty"] += 1
        
        elif operation == "standardize_headers":
            result_df = _standardize_headers(result_df)
            counts["standardize_headers"] += 1
        
        elif operation == "date_to_ddmmyyyy":
            result_df, converted = _convert_dates_to_ddmmyyyy(result_df, target_cols)
            if converted:
                counts["date_conversion"] += 1
        
        elif operation == "normalize_phone":
            result_df, normalized = _normalize_phone_numbers(result_df, target_cols)
            if normalized:
                counts["phone_normalization"] += 1
        
        elif operation == "validate_email":
            result_df, flagged = _validate_and_flag_emails(result_df, target_cols)
            if flagged is not None:
                counts["email_validation"] += flagged
        
        elif operation == "flag_invalid":
            result_df, flagged = _flag_invalid_values(result_df, target_cols)
            if flagged is not None:
                counts["invalid_flagged"] += flagged
    
    return result_df, counts


def _trim_spaces(df: pd.DataFrame) -> pd.DataFrame:
    """Trim leading/trailing string values in all cells."""
    result = df.copy()
    for col in result.columns:
        # Trim string values (dtype can be object or str)
        if result[col].dtype in [object, "object", "str"] or str(result[col].dtype).startswith('str'):
            result[col] = result[col].apply(
                lambda x: x.strip() if isinstance(x, str) else x
            )
    return result


def _remove_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows that are completely empty (all NaN)."""
    return df.dropna(how="all")


def _remove_empty_cols(df: pd.DataFrame) -> pd.DataFrame:
    """Remove columns that are completely empty (all NaN)."""
    return df.dropna(axis=1, how="all")


def _standardize_headers(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names: trim, lowercase, underscores."""
    df = df.copy()
    df.columns = [
        _normalize_name(str(col)) for col in df.columns
    ]
    # Remove duplicate column names after standardization
    df = _remove_duplicate_columns(df)
    return df


def _convert_dates_to_ddmmyyyy(
    df: pd.DataFrame,
    target_columns: Optional[List[str]],
) -> Tuple[pd.DataFrame, int]:
    """Convert date columns to DD-MM-YYYY format."""
    result = df.copy()
    converted_count = 0
    
    target_set = set(target_columns) if target_columns else set(result.columns)
    
    for col in result.columns:
        if col not in target_set:
            continue
        
        if result[col].dtype == object:
            try:
                # Try to convert to datetime
                dates = pd.to_datetime(result[col], dayfirst=True, errors="coerce")
                # Only convert if more than half the values are valid dates
                if dates.notna().sum() / len(dates) > 0.5 if len(dates) > 0 else False:
                    # Format as DD-MM-YYYY
                    result[col] = dates.dt.strftime(DEFAULT_DATE_FORMAT)
                    converted_count += 1
            except Exception:
                pass
    
    return result, converted_count


def _normalize_phone_numbers(
    df: pd.DataFrame,
    target_columns: Optional[List[str]],
) -> Tuple[pd.DataFrame, int]:
    """Normalize phone numbers to a standard format."""
    import re
    
    result = df.copy()
    normalized_count = 0
    
    target_set = set(target_columns) if target_columns else set(result.columns)
    
    phone_pattern = r"^\+?[1-9]\d{7,14}$"
    
    for col in result.columns:
        if col not in target_set:
            continue
        
        if result[col].dtype == object:
            # Apply phone normalization: strip non-digits, keep leading +
            def normalize_phone(val):
                if not isinstance(val, str):
                    return val
                # Remove all non-digit characters except leading +
                cleaned = re.sub(r"[^\d+]", "", val.strip())
                # Return cleaned digits (MVP: just return digits, full formatting optional)
                return cleaned if cleaned else val
            
            result[col] = result[col].apply(normalize_phone)
            # Count how many had phone-like values (simplified)
            normalized_count += sum(
                1 for val in result[col] 
                if isinstance(val, str) and re.match(phone_pattern, val.strip())
            )
    
    return result, normalized_count


def _validate_and_flag_emails(
    df: pd.DataFrame,
    target_columns: Optional[List[str]],
) -> Tuple[pd.DataFrame, int]:
    """Validate email format and flag invalid ones."""
    import re
    
    result = df.copy()
    flagged_count = 0
    
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    target_set = set(target_columns) if target_columns else set(result.columns)
    
    for col in result.columns:
        if col not in target_set:
            continue
        
        if result[col].dtype == object:
            def flag_invalid_email(val):
                nonlocal flagged_count
                if not isinstance(val, str):
                    return val
                if not re.match(email_pattern, val.strip()):
                    flagged_count += 1
                    return f"{val} ⚠invalid"
                return val
            
            result[col] = result[col].apply(flag_invalid_email)
    
    return result, flagged_count


def _flag_invalid_values(
    df: pd.DataFrame,
    target_columns: Optional[List[str]],
) -> Tuple[pd.DataFrame, int]:
    """Flag cells that contain obviously invalid values."""
    result = df.copy()
    flagged_count = 0
    
    target_set = set(target_columns) if target_columns else set(result.columns)
    
    for col in result.columns:
        if col not in target_set:
            continue
        
        if result[col].dtype == object:
            def flag_cell(val):
                nonlocal flagged_count
                if val is None or val == "":
                    return val
                # Flag if value looks like empty placeholder
                if val.strip().lower() in {"n/a", "na", "null", "none", "tbd", "pending"}:
                    flagged_count += 1
                    return f"⚠{str(val)}"
                return val
            
            result[col] = result[col].apply(flag_cell)
    
    return result, flagged_count