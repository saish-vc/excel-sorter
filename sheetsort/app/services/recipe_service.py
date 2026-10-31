"""Service for managing recipes (save, load, update, delete, apply)."""
from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

from sheetsort.app.models.recipe import create_recipe, Recipe
from sheetsort.app.models.audit_log_entry import create_audit_log_entry


class RecipeService:
    """Handles recipe storage and retrieval using SQLite."""
    
    def __init__(self, db_path: str = "recipes.db"):
        self.db_path = db_path
        Path(db_path).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize the SQLite database and create tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
                recipe_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                created_ts TEXT NOT NULL,
                sort_rules TEXT,  -- JSON
                filter_rules TEXT,  -- JSON
                cleaning_rules TEXT,  -- JSON
                split_rule TEXT,  -- JSON
                description TEXT,
                is_active INTEGER DEFAULT 0
            )
        """)
        # Also create audit log table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                entry_id TEXT PRIMARY KEY,
                user_action TEXT NOT NULL,
                file_id TEXT,
                recipe_id TEXT,
                timestamp TEXT NOT NULL,
                rows_processed INTEGER DEFAULT 0,
                rows_exported INTEGER DEFAULT 0,
                notes TEXT
            )
        """)
        conn.commit()
        conn.close()
    
    def save_recipe(
        self,
        name: str,
        sort_rules: List[Dict],
        filter_rules: List[Dict],
        cleaning_rules: List[Dict],
        split_rule: Optional[Dict],
        description: Optional[str] = None,
    ) -> str:
        """Save a new recipe to the database.
        
        Returns the recipe_id.
        """
        recipe_id = str(uuid.uuid4())
        created_ts = datetime.now().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        sort_rules_json = json.dumps(sort_rules) if sort_rules else "[]"
        filter_rules_json = json.dumps(filter_rules) if filter_rules else "[]"
        cleaning_rules_json = json.dumps(cleaning_rules) if cleaning_rules else "[]"
        split_rule_json = json.dumps(split_rule) if split_rule else "None"
        
        cursor.execute(
            """INSERT INTO recipes 
               (recipe_id, name, created_ts, sort_rules, filter_rules, 
                cleaning_rules, split_rule, description, is_active)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                recipe_id,
                name,
                created_ts,
                sort_rules_json,
                filter_rules_json,
                cleaning_rules_json,
                split_rule_json,
                description,
                0,  # is_active
            )
        )
        
        conn.commit()
        conn.close()
        
        # Log the action
        self._log_audit_action("recipe_save", recipe_id=recipe_id, notes=f"Recipe '{name}' saved")
        
        return recipe_id
    
    def load_recipe(self, recipe_id: str) -> Optional[Recipe]:
        """Load a recipe from the database by ID.
        
        Returns a Recipe dict or None if not found.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM recipes WHERE recipe_id = ?",
            (recipe_id,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row is None:
            return None
        
        # Unpack columns
        columns = ["recipe_id", "name", "created_ts", "sort_rules", 
                   "filter_rules", "cleaning_rules", "split_rule", 
                   "description", "is_active"]
        
        recipe_dict = dict(zip(columns, row))
        
        # Parse JSON fields
        try:
            recipe_dict["sort_rules"] = json.loads(recipe_dict["sort_rules"]) if recipe_dict["sort_rules"] else []
        except (json.JSONDecodeError, TypeError):
            recipe_dict["sort_rules"] = []
        
        try:
            recipe_dict["filter_rules"] = json.loads(recipe_dict["filter_rules"]) if recipe_dict["filter_rules"] else []
        except (json.JSONDecodeError, TypeError):
            recipe_dict["filter_rules"] = []
        
        try:
            recipe_dict["cleaning_rules"] = json.loads(recipe_dict["cleaning_rules"]) if recipe_dict["cleaning_rules"] else []
        except (json.JSONDecodeError, TypeError):
            recipe_dict["cleaning_rules"] = []
        
        try:
            recipe_dict["split_rule"] = json.loads(recipe_dict["split_rule"]) if recipe_dict["split_rule"] != "None" else None
        except (json.JSONDecodeError, TypeError):
            recipe_dict["split_rule"] = None
        
        return recipe_dict
    
    def update_recipe(
        self,
        recipe_id: str,
        name: Optional[str] = None,
        sort_rules: Optional[List[Dict]] = None,
        filter_rules: Optional[List[Dict]] = None,
        cleaning_rules: Optional[List[Dict]] = None,
        split_rule: Optional[Dict] = None,
        description: Optional[str] = None,
    ) -> bool:
        """Update an existing recipe.
        
        Returns True if updated, False if recipe not found.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if recipe exists
        cursor.execute("SELECT recipe_id FROM recipes WHERE recipe_id = ?", (recipe_id,))
        if cursor.fetchone() is None:
            conn.close()
            return False
        
        # Build update query dynamically
        updates = []
        params = []
        
        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if sort_rules is not None:
            updates.append("sort_rules = ?")
            params.append(json.dumps(sort_rules))
        if filter_rules is not None:
            updates.append("filter_rules = ?")
            params.append(json.dumps(filter_rules))
        if cleaning_rules is not None:
            updates.append("cleaning_rules = ?")
            params.append(json.dumps(cleaning_rules))
        if split_rule is not None:
            updates.append("split_rule = ?")
            params.append(json.dumps(split_rule))
        if description is not None:
            updates.append("description = ?")
            params.append(description)
        
        if not updates:
            conn.close()
            return True  # Nothing to update, but exists
        
        params.append(recipe_id)
        query = f"UPDATE recipes SET {', '.join(updates)} WHERE recipe_id = ?"
        cursor.execute(query, params)
        
        conn.commit()
        conn.close()
        
        # Log the action
        self._log_audit_action("recipe_update", recipe_id=recipe_id, notes=f"Recipe '{recipe_id}' updated")
        
        return True
    
    def delete_recipe(self, recipe_id: str) -> bool:
        """Delete a recipe from the database.
        
        Returns True if deleted, False if not found.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if recipe exists
        cursor.execute("SELECT recipe_id FROM recipes WHERE recipe_id = ?", (recipe_id,))
        if cursor.fetchone() is None:
            conn.close()
            return False
        
        # Also log what recipe was deleted (name)
        cursor.execute("SELECT name FROM recipes WHERE recipe_id = ?", (recipe_id,))
        row = cursor.fetchone()
        recipe_name = row[0] if row else "Unknown"
        
        cursor.execute("DELETE FROM recipes WHERE recipe_id = ?", (recipe_id,))
        conn.commit()
        conn.close()
        
        # Log the action
        self._log_audit_action("recipe_delete", recipe_id=recipe_id, notes=f"Recipe '{recipe_name}' deleted")
        
        return True
    
    def list_recipes(self) -> List[Dict[str, Any]]:
        """List all recipes in the database.
        
        Returns list of recipe summary dicts.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT recipe_id, name, created_ts, is_active FROM recipes"
        )
        rows = cursor.fetchall()
        conn.close()
        
        recipes = []
        for row in rows:
            recipes.append({
                "recipe_id": row[0],
                "name": row[1],
                "created_ts": row[2],
                "is_active": bool(row[3]),
            })
        
        return recipes
    
    def apply_recipe(
        self,
        recipe_id: str,
        df: pd.DataFrame,
        recipe_service: "RecipeService" = None,
    ) -> Tuple[pd.DataFrame, Dict[str, any]]:
        """Apply a stored recipe to a DataFrame.
        
        Returns (processed_df, applied_rules_summary).
        """
        recipe = self.load_recipe(recipe_id)
        if recipe is None:
            return df, {"error": "Recipe not found"}
        
        result = df.copy()
        applied = {"sort_rules": [], "filter_rules": [], "cleaning_rules": [], "split_rule": None}
        
        # Apply sorting
        sort_rules = recipe.get("sort_rules", [])
        if sort_rules:
            from sheetsort.app.services.sorting import apply_sorting
            result, had_sorting = apply_sorting(result, sort_rules)
            applied["sort_rules"] = sort_rules
        
        # Apply cleaning
        cleaning_rules = recipe.get("cleaning_rules", [])
        if cleaning_rules:
            from sheetsort.app.services.data_cleaning import apply_cleaning_rules
            result, cleaning_counts = apply_cleaning_rules(result, cleaning_rules)
            applied["cleaning_rules"] = [r.get("operation") for r in cleaning_rules]
        
        # Apply filters
        filter_rules = recipe.get("filter_rules", [])
        if filter_rules:
            from sheetsort.app.services.filtering import apply_filters
            result, filter_counts = apply_filters(result, filter_rules)
            applied["filter_rules"] = [r.get("condition") for r in filter_rules]
        
        # Apply splitting
        split_rule = recipe.get("split_rule")
        if split_rule:
            applied["split_rule"] = split_rule
        
        # Log the action
        self._log_audit_action("recipe_load", recipe_id=recipe_id, 
                              notes=f"Recipe '{recipe.get('name')}' applied", 
                              file_id=None)
        
        return result, applied

    def log_action(
        self,
        user_action: str,
        file_id: Optional[str] = None,
        recipe_id: Optional[str] = None,
        notes: Optional[str] = None,
        rows_processed: int = 0,
        rows_exported: int = 0,
    ) -> None:
        """Record a non-recipe audit event."""
        self._log_audit_action(
            user_action, file_id, recipe_id, notes, rows_processed, rows_exported
        )
    
    def _log_audit_action(
        self,
        user_action: str,
        file_id: Optional[str] = None,
        recipe_id: Optional[str] = None,
        notes: Optional[str] = None,
        rows_processed: int = 0,
        rows_exported: int = 0,
    ):
        """Log an audit action to the SQLite database."""
        import datetime
        
        entry_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO audit_log 
               (entry_id, user_action, file_id, recipe_id, timestamp, 
                rows_processed, rows_exported, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                entry_id,
                user_action,
                file_id,
                recipe_id,
                timestamp,
                rows_processed,
                rows_exported,
                notes,
            )
        )
        conn.commit()
        conn.close()
