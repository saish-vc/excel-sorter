# 📖 SheetSort: Administrative Staff User Guide

Welcome to **SheetSort**! This guide walks you through every screen and capability in the application.

---

## 🧭 Navigation Overview

SheetSort features a straightforward sidebar menu on the left:
1. **📁 Upload & Preview:** Load raw Excel or CSV files.
2. **🔍 Schema Detection:** Identify header rows and detect column types.
3. **🧹 Cleaning:** Clean text, dates, phones, and emails.
4. **📊 Sorting:** Multi-column sorting and custom branch priorities.
5. **🎯 Filtering:** Filter rows by numeric thresholds, dates, or keywords.
6. **🗑️ Deduplication:** Find and remove duplicate student records.
7. **✂️ Splitting:** Break a master list into department/branch sub-sheets.
8. **📤 Export & Recipes:** Save workflows and download polished Excel workbooks.
9. **📋 Audit Log:** Review the history of past exports and operations.

---

## 1. Upload & Preview
- Click **Browse files** or drag and drop your spreadsheet (`.xlsx`, `.xls`, or `.csv`).
- The application automatically validates file integrity and size (up to 50 MB / 100,000 rows).
- Check the **Data Preview** table to confirm row and column counts.

---

## 2. Schema Detection
- Many college reports contain 1 to 4 banner rows at the top (e.g., *"XYZ College of Engineering - Semester VII Marks"*).
- Leave the field on auto-detect or type the suspected row index, then click **Detect Header Row**.
- SheetSort automatically infers column types:
  - `id`: Student Roll Numbers, Registration IDs.
  - `date`: Admission dates, exam dates.
  - `email`: Student emails.
  - `phone`: Contact numbers.
  - `number`: Marks, CGPA, attendance percentages.
- You can override any detected type using the dropdown menus.

---

## 3. Data Cleaning
Select any combination of standardizing operations:
- **Trim leading/trailing spaces:** Strips hidden spaces before or after student names.
- **Remove empty rows / columns:** Deletes blank rows created by faulty exports.
- **Standardize headers:** Converts column names to clean `snake_case` (e.g. `"Student Name "` $\rightarrow$ `"student_name"`).
- **Convert dates to DD-MM-YYYY:** Unifies mixed date formats (`2026/05/12`, `12-May-2026` $\rightarrow$ `12-05-2026`).
- **Normalize phone numbers:** Removes parentheses, spaces, and hyphens to leave clean 10-digit mobile numbers.
- **Validate and flag emails:** Highlights malformed email addresses with a `⚠invalid` warning.
- **Flag invalid values:** Identifies missing values like `N/A`, `NULL`, `TBD`.

Click **Apply Cleaning Operations** to transform the table instantly.

---

## 4. Multi-Column Sorting
- Click **Add Sort Rule** to choose a primary column (e.g. `Department`).
- Set Order to `ascending` or `descending`.
- **Custom Academic Priority:** Want Computer Science first, followed by Information Technology? Enter `CSE, IT, ECE, Mechanical` into the **Custom Order** field.
- Add secondary sort rules (e.g., sort by `Marks` descending within each department).

---

## 5. Filtering
- Add one or multiple filter conditions:
  - `contains`: Match keywords (e.g., find all students with `"Honors"`).
  - `exact`: Match exact codes (e.g., branch == `"CSE"`).
  - `gt` / `gte` / `lt` / `lte`: Numeric thresholds (e.g., `attendance_pct >= 75`).
  - `between`: Range boundaries (e.g., marks between `40` and `60`).
  - `date_range`: Filter between two calendar dates.
- Combine rules with **AND** (all must match) or **OR** (any can match) logic.

---

## 6. Duplicate Handling
- **Exact Duplicates:** Remove identical rows. Choose whether to keep the `first` or `last` entry.
- **Subset Deduplication:** Select specific columns to check (e.g., check for duplicate `roll_number` even if student addresses differ).
- **Near-Duplicate Detection:** Use fuzzy matching to detect students whose names or records differ by minor typos.

---

## 7. Departmental Splitting
- Need to distribute individual mark sheets to each department HOD?
- Choose **Split by column** $\rightarrow$ `Department`.
- Enter a sheet prefix (e.g., `Dept_`).
- Click **Split Data**. SheetSort breaks the master table into separate worksheets (`Dept_CSE`, `Dept_IT`, `Dept_ECE`, etc.).

---

## 8. Export & Recipes
- **Save Current Workflow as Recipe:** Enter a name (e.g. *"Semester Marks Processor"*) and description. Your entire configuration (cleaning + sorting + filtering + splitting) is saved permanently.
- **Applying a Saved Recipe:** Next month when a new file arrives, simply click **Apply Recipe** on the list. All steps execute in a single click!
- **Download Excel File:** Click **Generate Summary and Export**. SheetSort produces a formatted `.xlsx` workbook with:
  - Formatted bold and frozen headers.
  - Active Excel AutoFilters.
  - Optimized column widths.
  - Individual sub-sheets (if split was used).
  - An executive **Summary tab** documenting original vs. final rows, duplicates eliminated, and operations applied.

---

## 9. Audit Log
- Every action (upload, recipe run, export) is recorded with timestamps, file identifiers, and row counts in the local database.
- Provides compliance verification for university inspections (NAAC, NBA, NIRF audits).

