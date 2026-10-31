"""Processing result - outcome of a file-processing run."""
from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

ProcessingResult = Dict[str, object]
"""
Result returned after a full pipeline run.

Key           | Type                    | Description
--------------|-------------------------|------------------------------------------
output_path   | str                     # Path to exported .xlsx (None if cancelled)
summary       | Dict[str, object]      # See summary schema below
audit_entry_id| str                     # ID of the audit log row
status        | Literal['success', 'partial', 'failed']
"""


Summary = Dict[str, object]
"""
Summary of processing results.

Key           | Type                    | Description
--------------|-------------------------|------------------------------------------
original_rows | int                     # Before processing
final_rows    | int                     # After all operations
duplicates_removed | int             # Exact + near-duplicate count
blank_rows_removed | int             # Empty-row count
invalid_values_flagged | int           # How many cells/rows flagged
columns_modified | int                 # How many columns had changes applied
processed_ts  | datetime                # When processing completed
"""


def create_processing_result(
    output_path: str,
    summary: Summary,
    audit_entry_id: str,
    status: str = "success",
) -> ProcessingResult:
    """Create a new ProcessingResult dict."""
    return {
        "output_path": output_path,
        "summary": summary,
        "audit_entry_id": audit_entry_id,
        "status": status,
    }