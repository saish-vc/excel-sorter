"""Recipe - saved processing workflow."""
from __future__ import annotations

from datetime import datetime
from typing import List, Dict, Optional
from .sort_rule import SortRule
from .filter_rule import FilterRule
from .cleaning_rule import CleaningRule
from .split_rule import SplitRule

Recipe = Dict[str, object]
"""
A reusable processing workflow.

Key           | Type                    | Description
--------------|-------------------------|------------------------------------------
recipe_id     | str                     # UUID
name          | str                     # User-given name (e.g., "Exam Report")
created_ts    | datetime                # When the recipe was saved
sort_rules    | List[SortRule]          # May be empty
filter_rules  | List[FilterRule]        # May be empty
cleaning_rules| List[CleaningRule]      # May be empty
split_rule    | Optional[SplitRule]    # May be None
description   | Optional[str]          # Free-form note
is_active     | bool                    # Whether this is the active recipe
"""


def create_recipe(
    name: str,
    sort_rules: List[SortRule] = None,
    filter_rules: List[FilterRule] = None,
    cleaning_rules: List[CleaningRule] = None,
    split_rule: Optional[SplitRule] = None,
    description: Optional[str] = None,
    is_active: bool = False,
) -> Recipe:
    """Create a new Recipe dict."""
    import uuid
    return {
        "recipe_id": str(uuid.uuid4()),
        "name": name,
        "created_ts": datetime.now(),
        "sort_rules": sort_rules or [],
        "filter_rules": filter_rules or [],
        "cleaning_rules": cleaning_rules or [],
        "split_rule": split_rule,
        "description": description,
        "is_active": is_active,
    }