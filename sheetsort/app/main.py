"""SheetSort main application entry point."""
from __future__ import annotations

import os
import sys
import tempfile
import uuid
from datetime import datetime

import pandas as pd
import streamlit as st
import logging, os, sys

# Configure file-level logging for the executable
try:
    log_dir = os.path.join(os.path.expanduser("~"), "SheetSort")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "app.log")
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    logging.info("SheetSort application started")
except Exception:
    pass

# Add project root to path (handle both bundled and unbundled cases)
if getattr(sys, 'frozen', False):
    # Running as PyInstaller bundle
    bundle_dir = sys._MEIPASS
    if bundle_dir not in sys.path:
        sys.path.insert(0, bundle_dir)
else:
    # Running as normal Python script
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

from sheetsort.app.services.upload_service import validate_file, read_file_into_dataframe, process_upload
from sheetsort.app.services.schema_detection import detect_header_row, detect_column_data_types
from sheetsort.app.services.data_cleaning import apply_cleaning_rules
from sheetsort.app.services.sorting import apply_sorting
from sheetsort.app.services.filtering import apply_filters
from sheetsort.app.services.deduplication import detect_and_remove_duplicates
from sheetsort.app.services.splitting import split_dataframe_by_column
from sheetsort.app.services.recipe_service import RecipeService
from sheetsort.app.services.export_service import export_to_excel, create_summary_dict
from sheetsort.app.models.audit_log_entry import create_audit_log_entry
from sheetsort.app.utils.config import ALLOWED_EXTENSIONS, is_allowed_file, get_safe_db_path


# Page config
st.set_page_config(
    page_title="SheetSort - College Data Processing",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "df" not in st.session_state:
    st.session_state.df = None
if "column_metadata" not in st.session_state:
    st.session_state.column_metadata = None
if "processing_steps" not in st.session_state:
    st.session_state.processing_steps = []
if "recipe_service" not in st.session_state:
    db_path = get_safe_db_path()
    st.session_state.recipe_service = RecipeService(db_path)
if "current_recipe" not in st.session_state:
    st.session_state.current_recipe = None
if "export_summary" not in st.session_state:
    st.session_state.export_summary = None
if "original_row_count" not in st.session_state:
    st.session_state.original_row_count = 0
if "cleaning_rules" not in st.session_state:
    st.session_state.cleaning_rules = []
if "cleaning_counts" not in st.session_state:
    st.session_state.cleaning_counts = {}
if "split_rule" not in st.session_state:
    st.session_state.split_rule = None
if "split_dataframes" not in st.session_state:
    st.session_state.split_dataframes = []
if "duplicates_removed" not in st.session_state:
    st.session_state.duplicates_removed = 0


def sidebar_navigation():
    """Render the sidebar navigation."""
    st.sidebar.title("SheetSort Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Upload & Preview", "Schema Detection", "Cleaning", "Sorting", 
         "Filtering", "Deduplication", "Splitting", "Export & Recipes",
         "Audit Log"],
        index=0,
    )
    return page


def page_upload_preview():
    """Page 1: File upload and preview."""
    st.header("📁 Upload & Preview")
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["xlsx", "xls", "csv"],
        help="Accepted formats: .xlsx, .xls, .csv. Maximum 50 MB or 100,000 rows.",
    )
    
    if uploaded_file is not None:
        # Validate
        is_valid, error_msg = validate_file(uploaded_file.name, uploaded_file.getvalue())
        
        if not is_valid:
            st.error(error_msg)
        else:
            # Process upload
            with st.spinner("Processing upload..."):
                uploaded_file_meta, df, error_msg = process_upload(
                    uploaded_file.name, uploaded_file.getvalue()
                )
            
            if error_msg:
                st.error(error_msg)
            else:
                st.session_state.uploaded_file = uploaded_file_meta
                st.session_state.df = df
                st.session_state.original_row_count = len(df)
                st.session_state.duplicates_removed = 0
                st.session_state.cleaning_rules = []
                st.session_state.cleaning_counts = {}
                st.session_state.split_rule = None
                st.session_state.split_dataframes = []
                
                st.success(f"File uploaded successfully!")
                st.info(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
                
                # Preview first 10 rows
                st.subheader("Data Preview")
                st.dataframe(df.head(10), use_container_width=True)
                
                # Store for next pages
                st.session_state.uploaded_file = uploaded_file_meta
    
    # Show upload info if available
    if st.session_state.uploaded_file:
        st.divider()
        st.caption(f"File: {st.session_state.uploaded_file['original_name']}")
        st.caption(f"Uploaded: {st.session_state.uploaded_file['upload_ts'].strftime('%Y-%m-%d %H:%M')}")


def page_schema_detection():
    """Page 2: Schema detection."""
    st.header("🔍 Schema Detection")
    
    if st.session_state.df is None:
        st.warning("Please upload a file first.")
        return
    
    df = st.session_state.df
    
    # Header row detection
    st.subheader("Header Row Detection")
    suspected_row = st.number_input(
        "Enter suspected header row number (0-indexed), or leave auto-detect",
        min_value=0,
        max_value=min(4, len(df) - 1),
        value=None,
        step=1,
    )
    
    if st.button("Detect Header Row"):
        header_row, auto_detected = detect_header_row(df, suspected_row)
        st.success(f"Header row detected at index: {header_row} (auto-detected: {auto_detected})")
        
        # Detect column data types
        with st.spinner("Detecting column types..."):
            column_metadata, data_df = detect_column_data_types(df, header_row)
        
        st.session_state.column_metadata = column_metadata
        
        # Display results
        st.subheader("Detected Column Types")
        
        for meta in column_metadata:
            with st.expander(f"{meta['column_name']} ({meta['data_type']})"):
                st.write(f"Normalized name: {meta['normalized_name']}")
                st.write(f"Sample values: {meta['sample_values']}")
                st.write(f"Is header: {meta['is_header']}")
                
                # Allow user to override data type
                new_type = st.selectbox(
                    "Override data type",
                    ["text", "number", "date", "email", "phone", "id"],
                    index=["text", "number", "date", "email", "phone", "id"].index(meta['data_type']),
                    key=f"type_{meta['column_index']}",
                )
                # Update in place
                meta['data_type'] = new_type
        
        # Show the data DataFrame with proper headers
        st.subheader("Data View (with headers applied)")
        st.dataframe(data_df.head(10), use_container_width=True)
    
    # Show detected metadata if available
    if st.session_state.column_metadata:
        st.divider()
        if st.button("Use Detected Schema for Processing"):
            st.success("Schema ready for processing steps!")
            st.session_state.processing_steps.append("schema_detected")


def page_cleaning():
    """Page 3: Data cleaning."""
    st.header("🧹 Data Cleaning")
    
    if st.session_state.df is None:
        st.warning("Please upload a file first.")
        return
    
    df = st.session_state.df
    cleaning_rules = []
    
    st.subheader("Select Cleaning Operations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("Trim leading/trailing spaces", key="trim_spaces", on_change=lambda: None)
        st.checkbox("Remove empty rows", key="remove_empty_rows", on_change=lambda: None)
        st.checkbox("Remove empty columns", key="remove_empty_cols", on_change=lambda: None)
        st.checkbox("Standardize headers", key="standardize_headers", on_change=lambda: None)
    
    with col2:
        st.checkbox("Convert dates to DD-MM-YYYY", key="date_to_ddmmyyyy", on_change=lambda: None)
        st.checkbox("Normalize phone numbers", key="normalize_phone", on_change=lambda: None)
        st.checkbox("Validate and flag emails", key="validate_email", on_change=lambda: None)
        st.checkbox("Flag invalid/missing values", key="flag_invalid", on_change=lambda: None)
    
    # Generate cleaning rules from checkboxes
    from sheetsort.app.models.cleaning_rule import CleaningOperation, create_cleaning_rule
    
    all_rules = []
    
    if st.session_state.get("trim_spaces", False):
        all_rules.append(create_cleaning_rule("trim_spaces", target_columns=None))
    if st.session_state.get("remove_empty_rows", False):
        all_rules.append(create_cleaning_rule("remove_empty_rows", target_columns=None))
    if st.session_state.get("remove_empty_cols", False):
        all_rules.append(create_cleaning_rule("remove_empty_cols", target_columns=None))
    if st.session_state.get("standardize_headers", False):
        all_rules.append(create_cleaning_rule("standardize_headers", target_columns=None))
    if st.session_state.get("date_to_ddmmyyyy", False):
        all_rules.append(create_cleaning_rule("date_to_ddmmyyyy", target_columns=None))
    if st.session_state.get("normalize_phone", False):
        all_rules.append(create_cleaning_rule("normalize_phone", target_columns=None))
    if st.session_state.get("validate_email", False):
        all_rules.append(create_cleaning_rule("validate_email", target_columns=None))
    if st.session_state.get("flag_invalid", False):
        all_rules.append(create_cleaning_rule("flag_invalid", target_columns=None))
    
    if st.button("Apply Cleaning Operations"):
        if not all_rules:
            st.warning("Please select at least one cleaning operation.")
        else:
            with st.spinner("Applying cleaning operations..."):
                cleaned_df, counts = apply_cleaning_rules(st.session_state.df, all_rules)
            
            st.session_state.df = cleaned_df
            st.session_state.cleaning_rules = all_rules
            st.session_state.cleaning_counts = counts
            st.success("Cleaning operations applied!")
            
            # Display results
            st.subheader("Cleaning Results")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Rows", st.session_state.df.shape[0])
            with col2:
                st.metric("Columns", st.session_state.df.shape[1])
            with col3:
                st.metric("Operations Applied", len(all_rules))
            
            # Show per-operation counts
            if any(counts.values()):
                st.write("Operation counts:")
                for op, count in counts.items():
                    if count > 0:
                        st.write(f"  - {op}: {count}")
    
    # Show current DataFrame preview
    if st.session_state.df is not None:
        st.subheader("Current Data Preview")
        st.dataframe(st.session_state.df.head(10), use_container_width=True)


def page_sorting():
    """Page 4: Sorting."""
    st.header("📊 Sorting")
    
    if st.session_state.df is None:
        st.warning("Please upload a file first.")
        return
    
    df = st.session_state.df
    
    st.subheader("Configure Sort Rules")
    
    # Get column names from current DataFrame
    column_names = list(df.columns)
    
    # Add sort rule
    with st.expander("Add Sort Rule"):
        col_name = st.selectbox("Column", column_names, key="sort_col")
        order = st.radio("Order", ["ascending", "descending"], key="sort_order")
        custom_order = st.text_input(
            "Custom order (comma-separated, e.g., CSE,IT,ECE,Mechanical)",
            key="custom_order",
            help="Leave blank for numeric/alphabetical sorting."
        )
        try:
            custom_order_list = [x.strip() for x in custom_order.split(",") if x.strip()] if custom_order else None
        except (ValueError, AttributeError):
            custom_order_list = None
        
        priority = st.number_input("Priority", min_value=0, value=0, key="sort_priority")
        
        if st.button("Add Sort Rule"):
            from sheetsort.app.models.sort_rule import SortRule, create_sort_rule
            
            rule = create_sort_rule(
                column_name=col_name,
                order="asc" if order == "ascending" else "desc",
                custom_order=custom_order_list,
                priority=priority,
            )
            
            # Ensure we have a list in session state
            if "sort_rules" not in st.session_state:
                st.session_state.sort_rules = []
            
            st.session_state.sort_rules.append(rule)
            st.rerun()
    
    # Display existing sort rules
    if "sort_rules" in st.session_state and st.session_state.sort_rules:
        st.write("Current sort rules:")
        for i, rule in enumerate(st.session_state.sort_rules):
            with st.expander(f"Rule {i+1}: {rule['column_name']}"):
                order = st.radio(
                    "Order",
                    ["ascending", "descending"],
                    index=0 if rule['order'] == 'asc' else 1,
                    key=f"rule_order_{i}",
                )
                custom_order_display = ", ".join(rule.get('custom_order', [])) if rule.get('custom_order') else ""
                new_custom = st.text_input(
                    "Custom order",
                    value=custom_order_display,
                    key=f"rule_custom_{i}",
                )
                try:
                    new_custom_list = [x.strip() for x in new_custom.split(",") if x.strip()] if new_custom else None
                except (ValueError, AttributeError):
                    new_custom_list = None
                
                new_priority = st.number_input(
                    "Priority",
                    min_value=0,
                    value=rule.get('priority', 0),
                    key=f"rule_prio_{i}",
                )
                
                if st.button("Update Rule", key=f"update_rule_{i}"):
                    rule['order'] = "asc" if order == "ascending" else "desc"
                    rule['custom_order'] = new_custom_list
                    rule['priority'] = new_priority
                    st.rerun()
                
                if st.button("Remove Rule", key=f"remove_rule_{i}"):
                    st.session_state.sort_rules.pop(i)
                    st.rerun()
    
    # Apply sorting
    if st.session_state.sort_rules:
        if st.button("Apply Sorting"):
            with st.spinner("Applying sort rules..."):
                sorted_df, had_sorting = apply_sorting(st.session_state.df, st.session_state.sort_rules)
            
            st.session_state.df = sorted_df
            st.success(f"Sorting applied! {'Custom order used.' if any(r.get('custom_order') for r in st.session_state.sort_rules) else 'Standard sorting used.'}")
            
            st.subheader("Sorted Data Preview")
            st.dataframe(st.session_state.df.head(10), use_container_width=True)
    else:
        st.info("No sort rules configured. Use the expander above to add sort rules.")


def page_filtering():
    """Page 5: Filtering."""
    st.header("🔍 Filtering")
    
    if st.session_state.df is None:
        st.warning("Please upload a file first.")
        return
    
    df = st.session_state.df
    
    st.subheader("Configure Filter Rules")
    
    column_names = [""] + list(df.columns)  # Include "No filter" option
    
    with st.expander("Add Filter Rule"):
        col_name = st.selectbox("Column", column_names, key="filter_col")
        condition = st.selectbox(
            "Condition",
            ["contains", "exact", "gt", "gte", "lt", "lte", "between", "date_range"],
            key="filter_condition",
        )
        
        col1, col2 = st.columns(2)
        with col1:
            value = st.text_input("Value 1", key="filter_value1")
        with col2:
            value2 = st.text_input("Value 2 (for between/date_range)", key="filter_value2")
        
        logic = st.radio("Logic with other filters", ["AND", "OR"], key="filter_logic")
        
        if st.button("Add Filter Rule"):
            from sheetsort.app.models.filter_rule import FilterRule, create_filter_rule, FilterCondition
            
            # Convert condition string to enum
            condition_enum = FilterCondition(condition)
            
            rule = create_filter_rule(
                column_name=col_name if col_name else "",
                condition=condition_enum,
                value=value if value else None,
                value2=value2 if value2 else None,
                logic="and" if logic == "AND" else "or",
            )
            
            if "filter_rules" not in st.session_state:
                st.session_state.filter_rules = []
            
            st.session_state.filter_rules.append(rule)
            st.rerun()
    
    # Display existing filter rules
    if "filter_rules" in st.session_state and st.session_state.filter_rules:
        st.write("Current filter rules:")
        for i, rule in enumerate(st.session_state.filter_rules):
            with st.expander(f"Rule {i+1}: {rule['column_name']}"):
                condition = st.selectbox(
                    "Condition",
                    ["contains", "exact", "gt", "gte", "lt", "lte", "between", "date_range"],
                    index=["contains", "exact", "gt", "gte", "lt", "lte", "between", "date_range"].index(rule['condition']),
                    key=f"rule_cond_{i}",
                )
                new_value = st.text_input("Value 1", value=str(rule.get('value', '')), key=f"rule_val1_{i}")
                new_value2 = st.text_input("Value 2", value=str(rule.get('value2', '') or ''), key=f"rule_val2_{i}")
                
                new_logic = st.radio("Logic", ["AND", "OR"], index=0 if rule.get('logic') == 'and' else 1, key=f"rule_logic_{i}")
                
                if st.button("Update Rule", key=f"update_filter_{i}"):
                    from sheetsort.app.models.filter_rule import FilterCondition as FC
                    rule['condition'] = FC(condition)
                    rule['value'] = new_value if new_value else None
                    rule['value2'] = new_value2 if new_value2 else None
                    rule['logic'] = "and" if new_logic == "AND" else "or"
                    st.rerun()
                
                if st.button("Remove Rule", key=f"remove_filter_{i}"):
                    st.session_state.filter_rules.pop(i)
                    st.rerun()
    
    # Apply filters
    if st.session_state.filter_rules:
        if st.button("Apply Filters"):
            with st.spinner("Applying filters..."):
                filtered_df, row_reduced = apply_filters(st.session_state.df, st.session_state.filter_rules)
            
            st.session_state.df = filtered_df
            st.success(f"Filters applied! {row_reduced} rows removed.")
            
            st.subheader("Filtered Data Preview")
            st.dataframe(st.session_state.df.head(10), use_container_width=True)
    else:
        st.info("No filter rules configured.")


def page_deduplication():
    """Page 6: Duplicate handling."""
    st.header("🗑️ Duplicate Handling")
    
    if st.session_state.df is None:
        st.warning("Please upload a file first.")
        return
    
    df = st.session_state.df
    
    st.subheader("Duplicate Detection Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        keep_option = st.radio("Keep", ["first", "last"], help="Which duplicate to keep")
        subset_cols = st.multiselect(
            "Subset columns (optional)",
            list(df.columns),
            help="Only consider these columns for duplicate detection"
        )
    
    with col2:
        detect_near = st.checkbox("Detect near-duplicates")
        if detect_near:
            near_subset = st.multiselect(
                "Near-duplicate columns",
                list(df.columns),
                help="Columns to compare for near-duplicate detection"
            )
            threshold = st.slider(
                "Similarity threshold",
                0.5, 0.99, 0.9,
                help="Rows with >= this similarity are considered near-duplicates"
            )
        else:
            near_subset = None
            threshold = 0.9
    
    if st.button("Apply Duplicate Removal"):
        from sheetsort.app.services.deduplication import detect_and_remove_duplicates
        
        with st.spinner("Detecting and removing duplicates..."):
            deduped_df, exact_removed, near_removed, details = detect_and_remove_duplicates(
                df,
                keep=keep_option,
                subset=subset_cols if subset_cols else None,
                detect_near_duplicates=detect_near,
                near_duplicates_subset=near_subset,
                near_duplicates_threshold=threshold,
            )
        
        st.session_state.df = deduped_df
        st.session_state.duplicates_removed += exact_removed + near_removed
        st.success(
            f"Duplicate removal complete! "
            f"Exact duplicates removed: {exact_removed}, "
            f"Near-duplicates removed: {near_removed}"
        )
        
        st.subheader("Result Data Preview")
        st.dataframe(st.session_state.df.head(10), use_container_width=True)
        
        # Show details
        if details:
            with st.expander("Duplicate Details"):
                for detail in details[:5]:  # Show first 5
                    st.write(detail)


def page_splitting():
    """Page 7: Splitting."""
    st.header("✂️ Split Data")
    
    if st.session_state.df is None:
        st.warning("Please upload a file first.")
        return
    
    df = st.session_state.df
    
    st.subheader("Split Settings")
    
    column_names = list(df.columns)
    split_column = st.selectbox("Split by column", column_names)
    
    split_prefix = st.text_input("Sheet name prefix", value="Dept_")
    include_header = st.checkbox("Include header in each sheet", value=True)
    
    if st.button("Split Data"):
        from sheetsort.app.services.splitting import split_dataframe_by_column
        from sheetsort.app.models.split_rule import SplitRule, create_split_rule
        
        split_rule = create_split_rule(
            by_column=split_column,
            sheet_name_prefix=split_prefix,
            include_header=include_header,
        )
        
        with st.spinner("Splitting data..."):
            dfs, split_info = split_dataframe_by_column(st.session_state.df, split_rule)
        st.session_state.split_rule = split_rule
        st.session_state.split_dataframes = dfs
        
        st.success(f"Data split into {split_info['total_sheets']} sheet(s)!")
        
        # Display each sheet
        for i, df_sheet in enumerate(dfs):
            st.write(f"**Sheet {i+1}** ({len(df_sheet)} rows)")
            st.dataframe(df_sheet.head(5), use_container_width=True)
            st.divider()
    
    # Also store split rule for recipe application
    if st.session_state.df is not None:
        if st.checkbox("Save split rule for recipe"):
            from sheetsort.app.services.recipe_service import RecipeService
            # This would be saved when user saves a recipe


def page_export_recipes():
    """Page 8: Export and Recipe management."""
    st.header("📤 Export & Recipe Management")
    
    if st.session_state.df is None:
        st.warning("Please process a file first.")
        return
    
    df = st.session_state.df
    
    # Recipe management section
    st.subheader("Recipe Management")
    
    # Recipe name
    recipe_name = st.text_input("Recipe name", value="")
    recipe_description = st.text_area("Description (optional)")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save Current Workflow as Recipe"):
            from sheetsort.app.models.sort_rule import SortRule
            from sheetsort.app.models.filter_rule import FilterRule
            from sheetsort.app.models.cleaning_rule import CleaningRule
            from sheetsort.app.models.split_rule import SplitRule
            
            # Gather current rules from session state
            sort_rules = st.session_state.get("sort_rules", [])
            filter_rules = st.session_state.get("filter_rules", [])
            cleaning_rules = st.session_state.cleaning_rules
            split_rule = st.session_state.split_rule
            
            # Save recipe
            recipe_id = st.session_state.recipe_service.save_recipe(
                name=recipe_name or "Unnamed Recipe",
                sort_rules=[{"column_name": r.get('column_name'), 'order': r.get('order'), 
                            'custom_order': r.get('custom_order'), 'priority': r.get('priority')} 
                           for r in sort_rules],
                filter_rules=[{"column_name": r.get('column_name'), 'condition': str(r.get('condition')), 
                              'value': r.get('value'), 'value2': r.get('value2'), 'logic': r.get('logic')} 
                             for r in filter_rules],
                cleaning_rules=cleaning_rules,
                split_rule=split_rule,
                description=recipe_description,
            )
            
            st.success(f"Recipe saved with ID: {recipe_id[:8]}...")
    
    with col2:
        if st.button("Load Recipe"):
            st.info("Please select a recipe from the list below.")
    
    # List recipes
    st.write("Your Recipes:")
    recipes = st.session_state.recipe_service.list_recipes()
    
    if recipes:
        for recipe in recipes:
            with st.expander(f"{recipe['name']} ({recipe['created_ts'][:10]})"):
                if st.button(f"Apply '{recipe['name']}'", key=f"apply_{recipe['recipe_id'][:8]}"):
                    from sheetsort.app.services.recipe_service import RecipeService
                    
                    # Load and apply
                    applied_df, applied_rules = st.session_state.recipe_service.apply_recipe(
                        recipe['recipe_id'], st.session_state.df
                    )
                    
                    st.session_state.df = applied_df
                    loaded_recipe = st.session_state.recipe_service.load_recipe(recipe["recipe_id"])
                    st.session_state.current_recipe = loaded_recipe
                    st.session_state.cleaning_rules = loaded_recipe.get("cleaning_rules", [])
                    st.session_state.split_rule = applied_rules.get("split_rule")
                    if st.session_state.split_rule:
                        st.session_state.split_dataframes, _ = split_dataframe_by_column(
                            applied_df, st.session_state.split_rule
                        )
                    st.success(f"Recipe '{recipe['name']}' applied!")
                    st.write("Applied rules summary:", applied_rules)
                    
                    # Rerun to update UI
                    st.rerun()
                if st.button(f"Update name/description", key=f"update_{recipe['recipe_id'][:8]}"):
                    st.session_state.recipe_service.update_recipe(
                        recipe["recipe_id"],
                        name=recipe_name or recipe["name"],
                        description=recipe_description or None,
                    )
                    st.success("Recipe updated.")
                    st.rerun()
                if st.button(f"Delete '{recipe['name']}'", key=f"delete_{recipe['recipe_id'][:8]}"):
                    st.session_state.recipe_service.delete_recipe(recipe["recipe_id"])
                    st.success("Recipe deleted.")
                    st.rerun()
    
    # Export section
    st.divider()
    st.subheader("Export Processed Data")
    
    if st.button("Generate Summary and Export"):
        from sheetsort.app.models.processing_result import create_processing_result, Summary
        from sheetsort.app.models.audit_log_entry import create_audit_log_entry
        
        # Create summary
        cleaning_counts = st.session_state.cleaning_counts
        summary = create_summary_dict(
            original_rows=st.session_state.original_row_count,
            final_rows=len(df),
            duplicates_removed=st.session_state.duplicates_removed,
            blank_rows_removed=cleaning_counts.get("remove_empty", 0),
            invalid_values_flagged=(
                cleaning_counts.get("email_validation", 0)
                + cleaning_counts.get("invalid_flagged", 0)
            ),
            columns_modified=sum(1 for value in cleaning_counts.values() if value),
        )
        
        # Create temporary output path (restricted to system temp dir)
        output_dir = tempfile.gettempdir()
        safe_filename = f"sheetsort_export_{uuid.uuid4().hex[:8]}.xlsx"
        output_path = os.path.join(output_dir, safe_filename)
        
        with st.spinner("Exporting to Excel..."):
            output_path, export_info = export_to_excel(
                df, summary, output_path,
                split_dataframes=st.session_state.split_dataframes,
            )
        st.session_state.recipe_service.log_action(
            "export",
            file_id=st.session_state.uploaded_file.get("file_id"),
            recipe_id=(
                st.session_state.current_recipe.get("recipe_id")
                if st.session_state.current_recipe else None
            ),
            rows_processed=st.session_state.original_row_count,
            rows_exported=len(df),
            notes="Excel report generated",
        )
        
        st.success("Export complete!")
        
        # Provide download
        with open(output_path, "rb") as f:
            st.download_button(
                label="Download Excel File",
                data=f.read(),
                file_name="sheetsort_output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        
        # Clean up temp file
        try:
            os.remove(output_path)
        except OSError:
            pass
        
        # Store summary for audit
        st.session_state.export_summary = export_info
    
    # Show export summary if available
    if st.session_state.export_summary:
        st.divider()
        st.write("Export Summary:")
        for key, value in st.session_state.export_summary.items():
            st.write(f"  - {key}: {value}")


def page_audit_log():
    """Page 9: Audit Log."""
    st.header("📋 Audit Log")
    
    import sqlite3
    from sheetsort.app.utils.config import AUDIT_LOG_MAX_ENTRIES
    
    db_path = get_safe_db_path()
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Count total entries
        cursor.execute("SELECT COUNT(*) FROM audit_log")
        total = cursor.fetchone()[0]
        
        # Get recent entries (last 20)
        cursor.execute("SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT 20")
        rows = cursor.fetchall()
        
        conn.close()
    except sqlite3.Error as e:
        st.error(f"Could not read audit log database.")
        return
    
    st.write(f"Total audit entries: {total}")
    
    if rows:
        # Define column headers
        headers = ["Entry ID", "Action", "File ID", "Recipe ID", "Timestamp", "Rows Processed", "Rows Exported", "Notes"]
        
        for row in rows:
            # Safely format timestamp string (stored as ISO text, not datetime obj)
            ts_display = str(row[4])[:16] if row[4] else "N/A"
            with st.expander(f"{row[1]} - {ts_display}"):
                cols = st.columns(len(headers))
                for i, header in enumerate(headers):
                    cols[i].write(f"{header}: {row[i]}")
    else:
        st.info("No audit entries yet.")


def main():
    """Main entry point for the SheetSort application."""
    page = sidebar_navigation()
    
    # Route to the appropriate page
    pages = {
        "Upload & Preview": page_upload_preview,
        "Schema Detection": page_schema_detection,
        "Cleaning": page_cleaning,
        "Sorting": page_sorting,
        "Filtering": page_filtering,
        "Deduplication": page_deduplication,
        "Splitting": page_splitting,
        "Export & Recipes": page_export_recipes,
        "Audit Log": page_audit_log,
    }
    
    if page in pages:
        pages[page]()
    else:
        st.error(f"Page '{page}' not found.")


if __name__ == "__main__":
    main()
