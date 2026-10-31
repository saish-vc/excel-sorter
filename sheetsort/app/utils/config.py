"""SheetSort configuration constants and defaults."""

from __future__ import annotations

import os
from pathlib import Path
from typing import List

# Base paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "sample_data"
LOGS_DIR = PROJECT_ROOT / "logs"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# File handling
ALLOWED_EXTENSIONS = {".xlsx", ".xls", ".csv"}
MAX_UPLOAD_ROWS = 100_000  # Safety limit for processing
MAX_UPLOAD_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB

# Column data-type defaults
DEFAULT_DATE_FORMAT = "%d-%m-%Y"
PHONE_NUMBER_REGEX = r"^\+?[1-9]\d{7,14}$"

# Recipe storage
RECIPE_DB_NAME = "recipes.db"

# Audit log
AUDIT_LOG_MAX_ENTRIES = 10_000  # Keep last N entries before archiving

# UI defaults
PREVIEW_ROW_COUNT = 10
DEFAULT_SORT_ORDER_ASC = "asc"
DEFAULT_SORT_ORDER_DESC = "desc"

# Logging
LOG_LEVEL = os.getenv("SHEETSORT_LOG_LEVEL", "INFO")
LOG_FORMAT = "%Y-%m-%d %H:%M:%S | %(levelname)-8s | %(name)s | %(message)s"


def is_allowed_file(filename: str) -> bool:
    """Check if a filename has an allowed extension."""
    if not filename:
        return False
    ext = Path(filename).suffix.lower()
    return ext in ALLOWED_EXTENSIONS


def get_upload_limit_info() -> dict:
    """Return human-readable upload limits."""
    return {
        "max_rows": MAX_UPLOAD_ROWS,
        "max_bytes": MAX_UPLOAD_SIZE_BYTES,
        "max_rows_label": f"{MAX_UPLOAD_ROWS:,} rows",
        "max_bytes_label": f"{MAX_UPLOAD_SIZE_BYTES // (1024 * 1024)} MB",
    }