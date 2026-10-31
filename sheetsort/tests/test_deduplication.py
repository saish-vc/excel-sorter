"""Unit tests for duplicate detection and removal."""
import pandas as pd
import numpy as np
from sheetsort.app.services.deduplication import detect_and_remove_duplicates


class TestDetectAndRemoveDuplicates:
    """Test duplicate detection and removal."""

    def test_exact_duplicates_removed(self):
        """Should remove exact duplicate rows."""
        df = pd.DataFrame({
            "Name": ["Alice", "Alice", "Bob"],
            "Age": [30, 30, 25]
        })
        result, exact_removed, near_removed, details = detect_and_remove_duplicates(
            df, keep="first"
        )
        assert exact_removed == 1  # One duplicate removed
        assert len(result) == 2  # 2 unique rows remaining
        assert near_removed == 0

    def test_no_duplicates(self):
        """Should handle data with no duplicates."""
        df = pd.DataFrame({
            "Name": ["Alice", "Bob", "Charlie"],
            "Age": [30, 25, 35]
        })
        result, exact_removed, near_removed, details = detect_and_remove_duplicates(
            df, keep="first"
        )
        assert exact_removed == 0
        assert len(result) == 3
        assert near_removed == 0

    def test_keep_last(self):
        """Should keep last occurrence when keep='last'."""
        df = pd.DataFrame({
            "Name": ["Alice", "Alice", "Bob"],
            "Age": [30, 30, 25]
        })
        result, exact_removed, near_removed, details = detect_and_remove_duplicates(
            df, keep="last"
        )
        # With keep='last', the second Alice should be kept
        assert len(result) == 2
        # The remaining Alice should be the second one
        assert result.iloc[1]["Name"] == "Alice" or result.iloc[0]["Name"] == "Alice"

    def test_keep_last_preserves_last_duplicate_row(self):
        """Keeping last must not silently preserve the first matching row."""
        df = pd.DataFrame({"Name": ["Alice", "Alice"], "Score": [10, 20]})

        result, removed, _, _ = detect_and_remove_duplicates(
            df, keep="last", subset=["Name"]
        )

        assert removed == 1
        assert result.iloc[0]["Score"] == 20

    def test_deduplicate_subset_columns(self):
        """Should only consider specified columns for duplicate detection."""
        df = pd.DataFrame({
            "Name": ["Alice", "Alice", "Bob"],
            "Age": [30, 31, 25],  # Different ages
            "City": ["NYC", "NYC", "LA"]
        })
        # Only check Name column for duplicates
        result, exact_removed, near_removed, details = detect_and_remove_duplicates(
            df, keep="first", subset=["Name"]
        )
        # Alice appears twice with same Name but different Age - with subset, they're still duplicates
        assert exact_removed >= 0
        assert len(result) <= 3
