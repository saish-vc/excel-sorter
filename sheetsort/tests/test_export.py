"""Unit tests for export functionality."""
import pandas as pd
import numpy as np
import tempfile
import os
from sheetsort.app.services.export_service import export_to_excel, create_summary_dict


class TestExportToExcel:
    """Test Excel export functionality."""

    def test_basic_export(self):
        """Should export DataFrame to Excel with Summary sheet."""
        df = pd.DataFrame({
            "Name": ["Alice", "Bob", "Charlie"],
            "Marks": [85, 92, 78]
        })

        summary = create_summary_dict(
            original_rows=3,
            final_rows=3,
            duplicates_removed=0,
            blank_rows_removed=0,
            invalid_values_flagged=0,
            columns_modified=0,
        )

        # Create a temp file
        tmpdir = tempfile.mkdtemp()
        output_path = os.path.join(tmpdir, "output.xlsx")

        try:
            result_path, export_info = export_to_excel(df, summary, output_path)

            # Check file was created
            assert os.path.exists(result_path)
            assert result_path == output_path

            # Check export info
            assert "rows_in" in export_info
            assert "rows_out" in export_info
            assert export_info["rows_in"] == 3
            assert export_info["rows_out"] == 3

            # Verify we can read it back
            read_df = pd.read_excel(result_path, sheet_name="Data")
            assert len(read_df) == 3
            assert list(read_df.columns) == ["Name", "Marks"]

            # Verify Summary sheet exists
            read_summary = pd.read_excel(result_path, sheet_name="Summary")
            assert len(read_summary) > 0

        finally:
            import shutil
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_export_with_duplicates_info(self):
        """Export should include duplicate removal info in summary."""
        df = pd.DataFrame({
            "Name": ["Alice", "Alice", "Bob"],
            "Marks": [85, 85, 78]
        })

        summary = create_summary_dict(
            original_rows=3,
            final_rows=2,  # One duplicate removed
            duplicates_removed=1,
            blank_rows_removed=0,
            invalid_values_flagged=0,
            columns_modified=0,
        )

        tmpdir = tempfile.mkdtemp()
        output_path = os.path.join(tmpdir, "output.xlsx")

        try:
            result_path, export_info = export_to_excel(df, summary, output_path)
            assert os.path.exists(result_path)

            # Verify summary stats are correct
            assert export_info["rows_in"] == 3
            assert export_info["rows_out"] == 2

        finally:
            import shutil
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_create_summary_dict(self):
        """Should create summary dictionary with correct keys."""
        summary = create_summary_dict(
            original_rows=100,
            final_rows=95,
            duplicates_removed=5,
            blank_rows_removed=3,
            invalid_values_flagged=2,
            columns_modified=1,
        )

        assert summary["original_rows"] == 100
        assert summary["final_rows"] == 95
        assert summary["duplicates_removed"] == 5
        assert summary["blank_rows_removed"] == 3
        assert summary["invalid_values_flagged"] == 2
        assert summary["columns_modified"] == 1


class TestExportFormatting:
    """Test that export includes proper formatting."""

    def test_export_has_required_sheets(self):
        """Exported file should have Data and Summary sheets."""
        df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})

        summary = create_summary_dict(original_rows=2, final_rows=2, duplicates_removed=0,
                                      blank_rows_removed=0, invalid_values_flagged=0,
                                      columns_modified=0)

        tmpdir = tempfile.mkdtemp()
        output_path = os.path.join(tmpdir, "output.xlsx")

        try:
            result_path, _ = export_to_excel(df, summary, output_path)

            # Check sheet names
            sheet_names = pd.ExcelFile(result_path).sheet_names
            assert "Data" in sheet_names
            assert "Summary" in sheet_names

        finally:
            import shutil
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_export_escapes_formula_like_cell_values(self):
        """Untrusted values must be exported as text, not executable formulas."""
        from openpyxl import load_workbook

        tmpdir = tempfile.mkdtemp()
        output_path = os.path.join(tmpdir, "output.xlsx")
        summary = create_summary_dict(1, 1, 0, 0, 0, 0)
        try:
            export_to_excel(pd.DataFrame({"Comment": ["=HYPERLINK(\"https://bad.example\")"]}), summary, output_path)
            workbook = load_workbook(output_path, data_only=False)
            assert workbook["Data"]["A2"].value.startswith("'")
        finally:
            import shutil
            shutil.rmtree(tmpdir, ignore_errors=True)
