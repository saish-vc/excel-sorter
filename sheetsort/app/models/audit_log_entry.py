"""Audit log entry - a single row in the audit log SQLite table."""
from __future__ import annotations

from datetime import datetime
from typing import Dict, Literal, Optional

AuditLogEntry = Dict[str, object]
"""
A single row in the audit log SQLite table.

Key           | Type                    | Description
--------------|-------------------------|------------------------------------------
entry_id      | str                     # UUID (primary key)
user_action   | Literal['upload', 'process', 'recipe_save', 'recipe_load', 'recipe_delete', 'export']  # What happened
file_id       | Optional[str]          # UUID of the uploaded file (if applicable)
recipe_id     | Optional[str]          # UUID of the recipe used (if applicable)
timestamp     | datetime                # When the action occurred
rows_processed| int                     # How many rows were in the input
rows_exported | int                     # How many rows made it to the output
notes         | Optional[str]          # Free-form notes (e.g., error type)
"""


def create_audit_log_entry(
    user_action: str,
    file_id: Optional[str] = None,
    recipe_id: Optional[str] = None,
    rows_processed: int = 0,
    rows_exported: int = 0,
    notes: Optional[str] = None,
) -> AuditLogEntry:
    """Create a new AuditLogEntry dict."""
    import uuid
    return {
        "entry_id": str(uuid.uuid4()),
        "user_action": user_action,
        "file_id": file_id,
        "recipe_id": recipe_id,
        "timestamp": datetime.now(),
        "rows_processed": rows_processed,
        "rows_exported": rows_exported,
        "notes": notes,
    }