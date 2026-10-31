"""Service for handling file uploads and initial validation."""
from __future__ import annotations

import uuid
import pandas as pd
from typing import Optional, Tuple

from sheetsort.app.utils.config import MAX_UPLOAD_ROWS, MAX_UPLOAD_SIZE_BYTES, is_allowed_file
from sheetsort.app.models.uploaded_file import create_uploaded_file, UploadedFile
from sheetsort.app.models.audit_log_entry import create_audit_log_entry


def validate_file(filename: str, content_bytes: bytes) -> Tuple[bool, Optional[str]]:
    """Validate an uploaded file's type and size.
    
    Returns (is_valid, error_message). If valid, error_message is None.
    """
    if not filename:
        return False, "No filename provided."
    
    if not is_allowed_file(filename):
        allowed = ", ".join(sorted(get_upload_limit_info().keys() if False else ["xlsx", "xls", "csv"]))
        return False, f"Unsupported file type. Please upload .xlsx, .xls, or .csv. Allowed: {allowed}"
    
    if len(content_bytes) > MAX_UPLOAD_SIZE_BYTES:
        return False, f"File too large. Maximum size is 50 MB."
    
    return True, None


def read_file_into_dataframe(filename: str, content_bytes: bytes) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """Read an uploaded file into a pandas DataFrame.
    
    Returns (df, error_message). If df is not None, error_message is None.
    """
    import io
    
    try:
        ext = filename.rsplit(".", 1)[-1].lower()
        if ext in ("xlsx", "xls"):
            # Read first sheet only for preview
            xls = pd.ExcelFile(io.BytesIO(content_bytes))
            df = pd.read_excel(io.BytesIO(content_bytes), sheet_name=0)
        elif ext == "csv":
            df = pd.read_csv(io.BytesIO(content_bytes))
        else:
            return None, "Unsupported file extension."
        
        if df.empty:
            return None, "The uploaded file is empty."

        if len(df) > MAX_UPLOAD_ROWS:
            return None, f"File has too many rows. Maximum is {MAX_UPLOAD_ROWS:,} rows."
        
        return df, None
    
    except pd.errors.EmptyDataError:
        return None, "The uploaded file is empty or contains no data."
    except Exception as e:
        return None, f"Could not read the file. Error: {str(e)[:100]}"


def process_upload(
    filename: str,
    content_bytes: bytes,
) -> Tuple[Optional[UploadedFile], Optional[pd.DataFrame], Optional[str]]:
    """Full upload processing: validate, read, create metadata.
    
    Returns (uploaded_file_metadata, dataframe, error_message).
    If successful, error_message is None.
    If error, both metadata and df are None.
    """
    # Validate
    is_valid, error_msg = validate_file(filename, content_bytes)
    if not is_valid:
        return None, None, error_msg
    
    # Read into DataFrame
    df, read_error = read_file_into_dataframe(filename, content_bytes)
    if read_error:
        return None, None, read_error
    
    # Create metadata
    file_id = str(uuid.uuid4())
    row_count = len(df)
    col_count = len(df.columns)
    
    uploaded_file_meta = create_uploaded_file(
        file_id=file_id,
        original_name=filename,
        file_type=filename.rsplit(".", 1)[-1].lower(),
        row_count=row_count,
        col_count=col_count,
    )
    
    return uploaded_file_meta, df, None
