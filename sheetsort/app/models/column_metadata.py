"""Column metadata - detected info per column."""
from __future__ import annotations

from typing import Dict, List, Optional, Literal

ColumnType = Literal['text', 'number', 'date', 'email', 'phone', 'id']

ColumnMetadata = Dict[str, object]
"""
Key            | Type                    | Description
---------------|-------------------------|------------------------------------------
column_name    | str                     # As detected (may be normalized)
column_index   | int                     # 0‑based position in data
data_type      | ColumnType              # Auto‑detected type
sample_values  | List[object]            # First 5 non‑null values for user review
is_header      | bool                    # Is this the header row?
normalized_name| str                     # Cleaned version (trimmed, lowercase, underscores)
"""


def create_column_metadata(
    column_name: str,
    column_index: int,
    data_type: ColumnType,
    sample_values: List[object],
    is_header: bool = True,
    normalized_name: Optional[str] = None,
) -> ColumnMetadata:
    """Create a new ColumnMetadata dict."""
    if normalized_name is None:
        normalized_name = _normalize_name(column_name)
    return {
        "column_name": column_name,
        "column_index": column_index,
        "data_type": data_type,
        "sample_values": sample_values,
        "is_header": is_header,
        "normalized_name": normalized_name,
    }


def _normalize_name(name: str) -> str:
    """Normalize a column name: trim, lowercase, replace spaces with underscores."""
    import re
    name = name.strip().lower()
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"_+", "_", name)
    return name