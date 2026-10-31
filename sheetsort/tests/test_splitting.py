"""Unit tests for splitting functionality."""
import pandas as pd
import numpy as np
from sheetsort.app.services.splitting import split_dataframe_by_column
from sheetsort.app.models.split_rule import create_split_rule


class TestSplitDataFrameByColumn:
    """Test splitting DataFrame by column."""

    def test_split_by_department(self):
        """Should split data by unique department values."""
        df = pd.DataFrame({
            "Department": ["CSE", "IT", "CSE", "ECE", "IT"],
            "Marks": [40, 30, 50, 20, 60],
            "Name": ["Alice", "Bob", "Charlie", "Dave", "Eve"]
        })

        split_rule = create_split_rule(
            by_column="Department",
            sheet_name_prefix="Dept_",
            include_header=True
        )

        dfs, split_info = split_dataframe_by_column(df, split_rule)

        # Should have 3 sheets (CSE, IT, ECE)
        assert split_info["total_sheets"] == 3
        assert split_info["total_rows"] == 5  # All rows accounted for

        # Check each sheet has correct data
        cse_sheet = dfs[0]  # First sheet should be CSE
        assert len(cse_sheet) == 2  # 2 CSE students
        assert set(cse_sheet["Department"].unique()) == {"CSE"}

    def test_split_by_single_column_one_value(self):
        """Should handle splitting when there's only one unique value."""
        df = pd.DataFrame({
            "Department": ["CSE", "CSE", "CSE"],
            "Marks": [40, 50, 60]
        })

        split_rule = create_split_rule(
            by_column="Department",
            sheet_name_prefix="Dept_",
            include_header=True
        )

        dfs, split_info = split_dataframe_by_column(df, split_rule)
        assert split_info["total_sheets"] == 1
        assert len(dfs[0]) == 3

    def test_split_preserves_columns(self):
        """Split should preserve all columns."""
        df = pd.DataFrame({
            "A": [1, 2, 3],
            "B": [4, 5, 6],
            "Group": ["X", "X", "Y"]
        })

        split_rule = create_split_rule(
            by_column="Group",
            sheet_name_prefix="Group_",
            include_header=True
        )

        dfs, split_info = split_dataframe_by_column(df, split_rule)
        assert split_info["total_sheets"] == 2
        # Each sheet should have columns A, B, Group
        for sheet in dfs:
            assert set(sheet.columns) == {"A", "B", "Group"}