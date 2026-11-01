"""Unit tests for filtering functionality."""
import pandas as pd
import numpy as np
from sheetsort.app.services.filtering import apply_filters
import pandas as pd
import numpy as np
from sheetsort.app.services.filtering import apply_filters
from sheetsort.app.models.filter_rule import create_filter_rule


class TestApplyFilters:
    """Test filtering operations."""

    def test_exact_match_filter(self):
        """Should filter by exact match."""
        df = pd.DataFrame({
            "Department": ["CSE", "IT", "CSE", "ECE"],
            "Marks": [40, 30, 50, 20]
        })
        rule = create_filter_rule(
            column_name="Department",
            condition="exact",
            value="CSE"
        )
        rules = [rule]
        result, reduced = apply_filters(df, rules)
        assert len(result) == 2  # 2 CSE rows
        assert all(result["Department"] == "CSE")

    def test_contains_filter(self):
        """Should filter by text contains."""
        df = pd.DataFrame({
            "Department": ["Computer Science", "IT", "CSE Electronics", "CSE Engineering"]
        })
        rule = create_filter_rule(
            column_name="Department",
            condition="contains",
            value="CSE"
        )
        rules = [rule]
        result, reduced = apply_filters(df, rules)
        # Should match "CSE Electronics" and "CSE Engineering"
        assert len(result) >= 2

    def test_greater_than_filter(self):
        """Should filter by numeric greater than."""
        df = pd.DataFrame({
            "Marks": [30, 60, 45, 20]
        })
        rule = create_filter_rule(
            column_name="Marks",
            condition="gt",
            value=40
        )
        rules = [rule]
        result, reduced = apply_filters(df, rules)
        assert len(result) == 2  # 60 and 45
        assert all(result["Marks"] > 40)

    def test_between_filter(self):
        """Should filter by numeric between."""
        df = pd.DataFrame({
            "Marks": [10, 30, 50, 70, 90]
        })
        rule = create_filter_rule(
            column_name="Marks",
            condition="between",
            value=30,
            value2=70
        )
        rules = [rule]
        result, reduced = apply_filters(df, rules)
        # Should include 30 and 70 (inclusive)
        assert len(result) >= 2

    def test_and_logic(self):
        """Should combine filters with AND logic."""
        df = pd.DataFrame({
            "Department": ["CSE", "CSE", "IT", "IT"],
            "Marks": [50, 60, 30, 70]
        })
        rule1 = create_filter_rule(
            column_name="Department",
            condition="exact",
            value="CSE",
            logic="and"
        )
        rule2 = create_filter_rule(
            column_name="Marks",
            condition="gt",
            value=45,
            logic="and"
        )
        rules = [rule1, rule2]
        result, reduced = apply_filters(df, rules)
        # CSE AND Marks > 45 should give 2 rows (CSE with 50 and 60)
        assert len(result) == 2
        assert result["Department"].iloc[0] == "CSE"

    def test_or_logic(self):
        """Should combine filters with OR logic."""
        df = pd.DataFrame({
            "Department": ["CSE", "CSE", "IT", "IT"],
            "Marks": [50, 60, 30, 70]
        })
        rule1 = create_filter_rule(
            column_name="Department",
            condition="exact",
            value="CSE",
            logic="or"
        )
        rule2 = create_filter_rule(
            column_name="Marks",
            condition="gt",
            value=55,
            logic="or"
        )
        rules = [rule1, rule2]
        result, reduced = apply_filters(df, rules)
        # CSE OR Marks > 55 should give 3 rows: CSE(50), CSE(60), IT(70)
        assert len(result) == 3


class TestFilteringNoRules:
    """Test filtering with no rules."""

    def test_no_rules_returns_unchanged(self):
        """Should return DataFrame unchanged when no rules provided."""
        df = pd.DataFrame({"A": [3, 1, 2]})
        result, reduced = apply_filters(df, [])
        pd.testing.assert_frame_equal(result, df)
        assert reduced == 0


class TestFilteringSecurity:
    """Security tests for filtering."""

    def test_contains_filter_with_regex_metacharacters(self):
        """Contains filter should NOT interpret regex metacharacters (ReDoS prevention)."""
        df = pd.DataFrame({
            "Name": ["Alice (admin)", "Bob", "Charlie [staff]", "Dave"]
        })
        # These characters would be regex metacharacters if regex=True
        rule = create_filter_rule(
            column_name="Name",
            condition="contains",
            value="(admin)"
        )
        result, reduced = apply_filters(df, [rule])
        assert len(result) == 1
        assert result["Name"].iloc[0] == "Alice (admin)"

    def test_contains_filter_with_evil_regex_pattern(self):
        """Ensure malicious regex patterns are treated as literal text."""
        df = pd.DataFrame({
            "Data": ["normal text", "a]b[c", "test.*data"]
        })
        rule = create_filter_rule(
            column_name="Data",
            condition="contains",
            value=".*"  # Would match everything if treated as regex
        )
        result, reduced = apply_filters(df, [rule])
        # Should only match "test.*data" literally
        assert len(result) == 1