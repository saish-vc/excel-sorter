"""Unit tests for recipe functionality."""
import pandas as pd
import numpy as np
import tempfile
import os
from sheetsort.app.services.recipe_service import RecipeService


class TestRecipeService:
    """Test recipe save/load/update/delete operations."""

    def setup_method(self):
        """Set up a temporary database for each test."""
        self.tmpdir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.tmpdir, "test_recipes.db")
        self.service = RecipeService(db_path=self.db_path)

    def teardown_method(self):
        """Clean up after each test."""
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_save_and_load_recipe(self):
        """Should save a recipe and load it back."""
        # Create a simple DataFrame to base a recipe on
        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

        # Save a recipe
        recipe_id = self.service.save_recipe(
            name="Test Recipe",
            sort_rules=[],
            filter_rules=[],
            cleaning_rules=[],
            split_rule=None,
            description="A test recipe for unit testing"
        )

        assert recipe_id is not None
        assert len(recipe_id) > 0

        # Load the recipe back
        loaded = self.service.load_recipe(recipe_id)
        assert loaded is not None
        assert loaded["name"] == "Test Recipe"
        assert loaded["description"] == "A test recipe for unit testing"
        assert loaded["recipe_id"] == recipe_id

    def test_list_recipes(self):
        """Should list recipes in the database."""
        # Initially empty
        recipes = self.service.list_recipes()
        assert len(recipes) == 0

        # Save a recipe
        self.service.save_recipe(
            name="Recipe 1",
            sort_rules=[],
            filter_rules=[],
            cleaning_rules=[],
            split_rule=None,
        )

        # List again
        recipes = self.service.list_recipes()
        assert len(recipes) == 1
        assert recipes[0]["name"] == "Recipe 1"

    def test_update_recipe(self):
        """Should update an existing recipe."""
        # Save a recipe
        recipe_id = self.service.save_recipe(
            name="Old Name",
            sort_rules=[],
            filter_rules=[],
            cleaning_rules=[],
            split_rule=None,
        )

        # Update it
        success = self.service.update_recipe(
            recipe_id=recipe_id,
            name="New Name",
        )

        assert success is True

        # Verify the update
        loaded = self.service.load_recipe(recipe_id)
        assert loaded["name"] == "New Name"

    def test_delete_recipe(self):
        """Should delete a recipe."""
        # Save a recipe
        recipe_id = self.service.save_recipe(
            name="To Be Deleted",
            sort_rules=[],
            filter_rules=[],
            cleaning_rules=[],
            split_rule=None,
        )

        # Verify it exists
        recipes = self.service.list_recipes()
        assert len(recipes) == 1

        # Delete it
        success = self.service.delete_recipe(recipe_id)

        assert success is True

        # Verify it's gone
        recipes = self.service.list_recipes()
        assert len(recipes) == 0

    def test_apply_recipe(self):
        """Should apply a stored recipe to a DataFrame."""
        # Save a recipe with a sort rule
        sort_rule = {"column_name": "A", "order": "asc", "custom_order": None, "priority": 0}
        recipe_id = self.service.save_recipe(
            name="Sort Recipe",
            sort_rules=[sort_rule],
            filter_rules=[],
            cleaning_rules=[],
            split_rule=None,
        )

        # Create a DataFrame unsorted
        df = pd.DataFrame({"A": [3, 1, 2], "B": [6, 9, 12]})

        # Apply the recipe
        applied_df, applied_rules = self.service.apply_recipe(
            recipe_id=recipe_id,
            df=df,
            recipe_service=self.service
        )

        # The data should be sorted by column A ascending
        assert list(applied_df["A"]) == [1, 2, 3]  # Sorted ascending

    def test_apply_nonexistent_recipe(self):
        """Should handle applying a recipe that doesn't exist."""
        df = pd.DataFrame({"A": [3, 1, 2]})

        applied_df, applied_rules = self.service.apply_recipe(
            recipe_id="nonexistent_id",
            df=df,
            recipe_service=self.service
        )

        # Should return the original DataFrame unchanged
        pd.testing.assert_frame_equal(applied_df, df)
        assert applied_rules.get("error") is not None or applied_rules == {}