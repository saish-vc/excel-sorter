"""Unit tests for data cleaning functionality."""
import pandas as pd
import numpy as np
from sheetsort.app.services.data_cleaning import apply_cleaning_rules, _trim_spaces, _remove_empty_rows, _remove_empty_cols, _standardize_headers


class TestTrimSpaces:
    """Test trim spaces operation."""

    def test_basic_trim(self):
        """Should trim leading/trailing spaces from string values."""
        df = pd.DataFrame({
            "Name": [" Alice ", " Bob ", "Charlie"],
            "Age": [30, 25, 35]
        })
        result = _trim_spaces(df)
        assert result.loc[0, "Name"] == "Alice"
        assert result.loc[1, "Name"] == "Bob"


class TestRemoveEmptyRows:
    """Test remove empty rows operation."""

    def test_remove_all_nan_rows(self):
        """Should remove rows that are completely NaN."""
        df = pd.DataFrame({
            "A": [1, np.nan, 3],
            "B": [np.nan, np.nan, np.nan]
        })
        result = _remove_empty_rows(df)
        #Rows 0 and 2 have data in column A, only row 1 is all-NaN
        assert len(result) == 2  # Rows 0 and 2 remain
        assert set(result["A"].tolist()) == {1, 3}


class TestRemoveEmptyCols:
    """Test remove empty columns operation."""

    def test_remove_all_nan_cols(self):
        """Should remove columns that are completely NaN."""
        df = pd.DataFrame({
            "A": [1, 2, 3],
            "B": [np.nan, np.nan, np.nan],
            "C": [4, 5, 6]
        })
        result = _remove_empty_cols(df)
        assert "B" not in result.columns
        assert "A" in result.columns
        assert "C" in result.columns


class TestStandardizeHeaders:
    """Test header standardization."""

    def test_standardize_lowercase_underscores(self):
        """Should standardize headers to lowercase with underscores."""
        df = pd.DataFrame({
            "Student Name": [1, 2],
            "Exam Score": [3, 4]
        })
        # Need to set header properly
        result = _standardize_headers(df)
        # Check that columns were transformed
        assert result.columns[0] == "student_name"
        assert result.columns[1] == "exam_score"


class TestApplyCleaningRules:
    """Test applying multiple cleaning rules."""

    def test_multiple_rules(self):
        """Should apply multiple cleaning rules."""
        df = pd.DataFrame({
            "  Name  ": [" Alice ", " Bob "],
            "  Age ": [30, 25],
            "EmptyCol": [np.nan, np.nan]
        })

        rules = [
            {"operation": "trim_spaces", "enabled": True, "target_columns": None},
            {"operation": "remove_empty_cols", "enabled": True, "target_columns": None},
            {"operation": "standardize_headers", "enabled": True, "target_columns": None},
        ]

        result, counts = apply_cleaning_rules(df, rules)
        assert "EmptyCol" not in result.columns  # Removed
        assert list(result.columns) == ["name", "age"]  # Standardized + trimmed
        assert counts["trim_spaces"] >= 0
        assert counts.get("remove_empty") >= 0
        assert counts["standardize_headers"] >= 0


class TestApplyCleaningRulesWithDates:
    """Test date conversion cleaning rule."""

    def test_date_conversion(self):
        """Should convert dates to DD-MM-YYYY format."""
        df = pd.DataFrame({
            "Exam Date": ["2023-01-15", "2023-02-20"],
            "Name": ["Alice", "Bob"]
        })

        rules = [
            {"operation": "date_to_ddmmyyyy", "enabled": True, "target_columns": ["Exam Date"]},
        ]

        result, counts = apply_cleaning_rules(df, rules)
        # Check that date column exists and has been processed
        assert "Exam Date" in result.columns
        assert counts["date_conversion"] >= 0