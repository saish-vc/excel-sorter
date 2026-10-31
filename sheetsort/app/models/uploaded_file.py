"""Metadata about an uploaded file.

Used to track the state of a user's upload throughout the processing pipeline.
"""
from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional, Literal

UploadedFile = Dict[str, object]
"""
Key            | Type                    | Description
---------------|-------------------------|------------------------------------------
file_id        | str                     # Unique UUID for this upload
original_name  | str                     # User-supplied filename
upload_ts      | datetime                # When the file was uploaded
row_count      | int                     # Total rows (incl. header)
col_count      | int                     # Total columns
file_type      | Literal['xlsx', 'xls', 'csv']  # Detected type
temp_path      | str                     # Path to temp copy (read-only, deleted after export)
status         | Literal['pending', 'processed', 'error']  # Processing state
error_message  | Optional[str]         # If status == 'error'
"""


def create_uploaded_file(
    file_id: str,
    original_name: str,
    file_type: str,
    row_count: int,
    col_count: int,
) -> UploadedFile:
    """Create a new UploadedFile metadata dict."""
    return {
        "file_id": file_id,
        "original_name": original_name,
        "upload_ts": datetime.now(),
        "row_count": row_count,
        "col_count": col_count,
        "file_type": file_type,
        "temp_path": "",
        "status": "pending",
        "error_message": None,
    }