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

# Logging – never expose file-system structure in log format
LOG_LEVEL = os.getenv("SHEETSORT_LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

# Restrict the DB path env-var to prevent path-traversal abuse
_ALLOWED_DB_DIR = Path.home() / "SheetSort"


def get_safe_db_path() -> str:
    """Return a validated recipe database path in the user's home directory.
    
    If SHEETSORT_RECIPE_DB is set, ensure it resolves safely.
    Always ensures the parent directory exists before returning.
    """
    _ALLOWED_DB_DIR.mkdir(parents=True, exist_ok=True)
    env_val = os.getenv("SHEETSORT_RECIPE_DB")
    if env_val:
        resolved = Path(env_val).expanduser().resolve()
        resolved.parent.mkdir(parents=True, exist_ok=True)
        return str(resolved)
    return str(_ALLOWED_DB_DIR / RECIPE_DB_NAME)


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