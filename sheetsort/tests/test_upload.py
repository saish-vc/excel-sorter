"""Unit tests for file upload functionality."""
import pytest
import pandas as pd
import tempfile
import os
from sheetsort.app.services.upload_service import validate_file, read_file_into_dataframe, process_upload


class TestValidateFile:
    """Test file type and size validation."""

    def test_valid_xlsx(self):
        """Valid .xlsx file should pass validation."""
        is_valid, error_msg = validate_file("test.xlsx", b"fake content")
        assert is_valid is True
        assert error_msg is None

    def test_valid_csv(self):
        """Valid .csv file should pass validation."""
        is_valid, error_msg = validate_file("test.csv", b"fake content")
        assert is_valid is True

    def test_valid_xls(self):
        """Valid .xls file should pass validation."""
        is_valid, error_msg = validate_file("test.xls", b"fake content")
        assert is_valid is True

    def test_invalid_extension(self):
        """Invalid file type should fail validation."""
        is_valid, error_msg = validate_file("test.txt", b"fake content")
        assert is_valid is False
        assert "Unsupported" in error_msg

    def test_no_filename(self):
        """No filename should fail validation."""
        is_valid, error_msg = validate_file(None, b"fake content")
        assert is_valid is False

    def test_too_large(self):
        """File too large should fail validation."""
        is_valid, error_msg = validate_file("test.xlsx", b"x" * (51 * 1024 * 1024))
        assert is_valid is False
        assert "too large" in error_msg.lower()


class TestReadFileIntoDataFrame:
    """Test reading files into DataFrames."""

    def test_valid_csv_content(self):
        """CSV content should be readable."""
        df, error = read_file_into_dataframe("test.csv", b"name,age\nAlice,30\nBob,25")
        assert error is None
        assert df is not None
        assert len(df) == 2
        assert list(df.columns) == ["name", "age"]

    def test_empty_csv(self):
        """Empty CSV should return error."""
        df, error = read_file_into_dataframe("test.csv", b"")
        assert error is not None
        assert "empty" in error.lower()

    def test_valid_xlsx_content(self, tmpdir):
        """Excel file should be readable (create actual file)."""
        # Create a temp xlsx file
        xlsx_path = os.path.join(tmpdir, "test.xlsx")
        df_original = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
        df_original.to_excel(xlsx_path, index=False)

        with open(xlsx_path, "rb") as f:
            content = f.read()

        df, error = read_file_into_dataframe("test.xlsx", content)
        assert error is None
        assert df is not None
        assert len(df) == 2


class TestProcessUpload:
    """Test full upload processing."""

    def test_valid_upload_creates_metadata(self):
        """Valid upload should create metadata."""
        # Create a simple CSV in memory
        csv_content = b"name,age\nAlice,30\nBob,25"
        meta, df, error = process_upload("test.csv", csv_content)

        assert error is None
        assert meta is not None
        assert meta["file_id"] is not None
        assert meta["original_name"] == "test.csv"
        assert meta["row_count"] == 2
        assert meta["col_count"] == 2
        assert df is not None
        assert len(df) == 2

    def test_upload_empty_file(self):
        """Empty file should return error."""
        meta, df, error = process_upload("test.csv", b"")
        assert error is not None
        assert meta is None
        assert df is None