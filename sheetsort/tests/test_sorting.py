"""Unit tests for sorting functionality."""
import pandas as pd
import numpy as np
from sheetsort.app.services.sorting import apply_sorting
from sheetsort.app.models.sort_rule import create_sort_rule


class TestApplySorting:
    """Test multi-column sorting."""

    def test_single_column_ascending(self):
        """Should sort single column ascending."""
        df = pd.DataFrame({
            " Marks": [30, 20, 40, 10]
        })
        rule = create_sort_rule(column_name=" Marks", order="asc")
        rules = [rule]
        result, had_sorting = apply_sorting(df, rules)
        assert result[" Marks"].tolist() == [10, 20, 30, 40]

    def test_single_column_descending(self):
        """Should sort single column descending."""
        df = pd.DataFrame({
            " Marks": [30, 20, 40, 10]
        })
        rule = create_sort_rule(column_name=" Marks", order="desc")
        rules = [rule]
        result, had_sorting = apply_sorting(df, rules)
        assert result[" Marks"].tolist() == [40, 30, 20, 10]

    def test_multi_column_sorting(self):
        """Should sort by multiple columns with priority."""
        df = pd.DataFrame({
            "Department": ["CSE", "IT", "CSE", "IT"],
            " Marks": [40, 30, 50, 20],
            "Name": ["Alice", "Bob", "Charlie", "Dave"]
        })
        rules = [
            create_sort_rule(column_name="Department", order="asc", priority=0),
            create_sort_rule(column_name=" Marks", order="desc", priority=1),
        ]
        result, had_sorting = apply_sorting(df, rules)
        # CSE first (alphabetical), then within CSE, sort by marks descending
        cse_rows = result[result["Department"] == "CSE"]
        assert cse_rows.iloc[0][" Marks"] == 50  # Highest marks in CSE
        assert cse_rows.iloc[1][" Marks"] == 40

    def test_custom_order_sorting(self):
        """Should sort by custom order."""
        df = pd.DataFrame({
            "Department": ["IT", "CSE", "ECE", "Mechanical"]
        })
        rule = create_sort_rule(
            column_name="Department",
            order="asc",
            custom_order=["CSE", "IT", "ECE", "Mechanical"]
        )
        rules = [rule]
        result, had_sorting = apply_sorting(df, rules)
        # CSE should come first
        assert result["Department"].iloc[0] == "CSE"
        # Verify full custom order: CSE, IT, ECE, Mechanical
        expected = ["CSE", "IT", "ECE", "Mechanical"]
        actual = result["Department"].tolist()
        assert actual == expected


class TestSortingNoRules:
    """Test sorting with no rules."""

    def test_no_rules_returns_unchanged(self):
        """Should return DataFrame unchanged when no rules provided."""
        df = pd.DataFrame({"A": [3, 1, 2]})
        result, had_sorting = apply_sorting(df, [])
        pd.testing.assert_frame_equal(result, df)
        assert had_sorting is False