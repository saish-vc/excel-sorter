"""Service for handling file uploads and initial validation."""
from __future__ import annotations

import uuid
import pandas as pd
from typing import Optional, Tuple

from sheetsort.app.utils.config import MAX_UPLOAD_ROWS, MAX_UPLOAD_SIZE_BYTES, is_allowed_file
from sheetsort.app.models.uploaded_file import create_uploaded_file, UploadedFile
from sheetsort.app.models.audit_log_entry import create_audit_log_entry

# Magic bytes for known file types
_XLSX_MAGIC = b"PK"  # ZIP-based Office Open XML
_XLS_MAGIC = b"\xd0\xcf\x11\xe0"  # OLE2 Compound Document
# CSV has no magic bytes, but must be valid UTF-8/Latin-1 text


def _validate_file_content(filename: str, content_bytes: bytes) -> Tuple[bool, Optional[str]]:
    """Validate that file content matches the claimed extension (magic-byte check).
    
    Prevents attackers from uploading malicious files disguised with an allowed extension.
    """
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    
    if ext == "xlsx":
        if not content_bytes[:2] == _XLSX_MAGIC:
            return False, "File content does not match .xlsx format. The file may be corrupted or spoofed."
    elif ext == "xls":
        if not content_bytes[:4] == _XLS_MAGIC:
            return False, "File content does not match .xls format. The file may be corrupted or spoofed."
    elif ext == "csv":
        # Basic check: CSV must be decodable as text
        try:
            content_bytes[:4096].decode("utf-8")
        except UnicodeDecodeError:
            try:
                content_bytes[:4096].decode("latin-1")
            except UnicodeDecodeError:
                return False, "File does not appear to be a valid text/CSV file."
    
    return True, None


def validate_file(filename: str, content_bytes: bytes) -> Tuple[bool, Optional[str]]:
    """Validate an uploaded file's type, size, and content integrity.
    
    Returns (is_valid, error_message). If valid, error_message is None.
    """
    if not filename:
        return False, "No filename provided."
    
    if not is_allowed_file(filename):
        return False, "Unsupported file type. Please upload .xlsx, .xls, or .csv."
    
    if len(content_bytes) > MAX_UPLOAD_SIZE_BYTES:
        return False, f"File too large. Maximum size is 50 MB."
    
    if len(content_bytes) == 0:
        return False, "Uploaded file is empty (0 bytes)."
    
    # Magic-byte / content-type validation
    content_valid, content_error = _validate_file_content(filename, content_bytes)
    if not content_valid:
        return False, content_error
    
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
        return None, f"Could not read the file. The file may be corrupted or in an unexpected format."


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
