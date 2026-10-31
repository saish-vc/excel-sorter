"""Service for exporting processed data to Excel files."""
from __future__ import annotations

import datetime
import pandas as pd
from typing import Tuple, Dict, Any, List, Optional

from sheetsort.app.models.processing_result import create_processing_result, Summary
from sheetsort.app.models.audit_log_entry import create_audit_log_entry


def export_to_excel(
    df: pd.DataFrame,
    summary: Summary,
    output_path: str,
    audit_entry: Optional[dict] = None,
    split_dataframes: Optional[List[pd.DataFrame]] = None,
) -> Tuple[str, Dict[str, any]]:
    """Export a DataFrame to an Excel file with a Summary sheet and formatting.
    
    The output file contains:
    - Sheet 1: "Data" - the cleaned/processed data with formatting
    - Sheet 2: "Summary" - processing summary statistics
    
    Formatting includes:
    - Bold header row
    - Frozen header row
    - Auto column width
    - Filters enabled
    
    Returns (output_path, export_info_dict).
    """
    import datetime
    
    # Create workbook with two sheets using openpyxl
    from openpyxl import Workbook
    from openpyxl.utils import get_column_letter
    from openpyxl.styles import Font, Alignment
    
    wb = Workbook()
    
    # ---- Sheet 1: Data ----
    ws_data = wb.active
    ws_data.title = "Data"
    
    # Write data with formatting
    # Add headers (bold, frozen)
    headers = list(df.columns)
    header_font = Font(bold=True)
    header_alignment = Alignment(wrap_text=True)
    
    # Write headers
    for col_idx, header in enumerate(headers, 1):
        cell = ws_data.cell(row=1, column=col_idx, value=header)
        cell.font = header_font
        cell.alignment = header_alignment
    
    def safe_excel_value(value: Any) -> Any:
        """Prevent spreadsheet formula execution from untrusted cell text."""
        if isinstance(value, str) and value.startswith(("=", "+", "-", "@")):
            return f"'{value}"
        return value

    # Write data rows
    for row_idx, (_, row) in enumerate(df.iterrows(), 2):
        for col_idx, value in enumerate(row, 1):
            cell = ws_data.cell(row=row_idx, column=col_idx, value=safe_excel_value(value))
    
    # Auto-fit column widths
    for col_idx in range(1, len(headers) + 1):
        max_length = 0
        for row_idx in range(1, min(len(df) + 2, 1000)):
            cell = ws_data.cell(row=row_idx, column=col_idx)
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        adjusted_width = max(max_length + 2, 10)
        ws_data.column_dimensions[get_column_letter(col_idx)].width = adjusted_width
    
    # Freeze the header row
    ws_data.freeze_panes = "A2"
    
    # Enable filters (AutoFilter)
    if headers:
        ws_data.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{len(df) + 1}"
    
    # Optional department/company/etc. sheets retain the same safe output rules.
    for sheet_number, split_df in enumerate(split_dataframes or [], 1):
        requested_name = str(split_df.attrs.get("sheet_name", f"Sheet_{sheet_number}"))
        worksheet = wb.create_sheet(requested_name[:31] or f"Sheet_{sheet_number}")
        for col_idx, header in enumerate(split_df.columns, 1):
            worksheet.cell(row=1, column=col_idx, value=header).font = header_font
        for row_idx, (_, row) in enumerate(split_df.iterrows(), 2):
            for col_idx, value in enumerate(row, 1):
                worksheet.cell(row=row_idx, column=col_idx, value=safe_excel_value(value))
        worksheet.freeze_panes = "A2"
        if len(split_df.columns):
            worksheet.auto_filter.ref = (
                f"A1:{get_column_letter(len(split_df.columns))}{len(split_df) + 1}"
            )

    # ---- Summary ----
    ws_summary = wb.create_sheet("Summary")
    
    summary_data = [
        ("Original Row Count", summary.get("original_rows", 0)),
        ("Final Row Count", summary.get("final_rows", 0)),
        ("Duplicates Removed", summary.get("duplicates_removed", 0)),
        ("Blank Rows Removed", summary.get("blank_rows_removed", 0)),
        ("Invalid Values Flagged", summary.get("invalid_values_flagged", 0)),
        ("Columns Modified", summary.get("columns_modified", 0)),
        ("Processed On", summary.get("processed_ts", datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S") if isinstance(summary.get("processed_ts"), datetime.datetime) else summary.get("processed_ts", "N/A")),
    ]
    
    for row_idx, (label, value) in enumerate(summary_data, 1):
        ws_summary.cell(row=row_idx, column=1, value=label).font = Font(bold=True)
        ws_summary.cell(row=row_idx, column=2, value=value)
    
    # Set column widths for summary
    ws_summary.column_dimensions['A'].width = 28
    ws_summary.column_dimensions['B'].width = 20
    
    # Save the workbook
    wb.save(output_path)
    
    # Create audit log entry
    audit_info = {
        "output_path": output_path,
        "rows_in": summary.get("original_rows", 0),
        "rows_out": summary.get("final_rows", 0),
    }
    
    if audit_entry:
        # Append additional audit info
        audit_info["notes"] = audit_entry.get("notes", "")
    
    return output_path, audit_info


def create_summary_dict(
    original_rows: int,
    final_rows: int,
    duplicates_removed: int,
    blank_rows_removed: int,
    invalid_values_flagged: int,
    columns_modified: int,
    processed_ts: Optional[datetime.datetime] = None,
) -> Summary:
    """Create a summary dictionary for export."""
    if processed_ts is None:
        processed_ts = datetime.datetime.now()
    
    return {
        "original_rows": original_rows,
        "final_rows": final_rows,
        "duplicates_removed": duplicates_removed,
        "blank_rows_removed": blank_rows_removed,
        "invalid_values_flagged": invalid_values_flagged,
        "columns_modified": columns_modified,
        "processed_ts": processed_ts,
    }
