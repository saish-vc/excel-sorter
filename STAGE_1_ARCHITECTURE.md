# Stage 1 — System Architecture and Design: SheetSort

## 1. Technology Stack Recommendation

### Recommended Stack ( justified )

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **Language** | **Python 3.11+** | Dominant data‑science ecosystem; pandas + openpyxl maturity; simple deployment; familiar to college IT staff |
| **Web Framework** | **Streamlit** | Zero‑config Python web app; automatic UI from data frames; built‑in file uploader; no separate frontend build step; ideal for internal/admin tools |
| **Data Manipulation** | **pandas** | Robust table handling; sorting/filtering/deduplication built‑in; efficient for 50K‑row datasets; expressive API |
| **Excel I/O** | **openpyxl** | Read/write .xlsx files; supports formatting (bold headers, frozen rows, auto‑width, filters) needed for export; widely adopted |
| **Storage** | **SQLite** | Zero‑config file‑based database; perfect for local/deployed college server; stores users, recipes, audit logs without external service |
| **Testing** | **pytest** | Simple, convention‑driven; automatic discovery; fixture support for uploaded files and recipes |
| **Containerisation** | **Docker** | Single‑command deployment; isolates dependencies; runs on Windows/macOS/Linux; ideal for college server environment |
| **Configuration** | **Python dotenv + .env file** | Environment‑variable driven (upload limits, paths); no hard‑coded secrets; easy to adjust per deployment |

### Why Not Alternatives ?

| Alternative | Reason for Rejection |
|-------------|----------------------|
| **Node.js + React** | Extra build step; state management overhead; unnecessary for data‑processing‑centric app |
| **PHP Laravel** | Weaker Excel/CSV ecosystem; pandas‑style data manipulation not native; over‑engineered for this use case |
| **R Shiny** | Smaller deployment community; licensing considerations; less familiar to typical college IT staff |
| **Full‑stack ERP integration up‑front** | Out of scope for MVP; would delay delivery; can be added in Phase 2 |

---

## 2. System Architecture Diagram (Mermaid Syntax)

```mermaid
flowchart TD
    %% UI Layer
    subgraph UI [Browser / Streamlit Frontend]
        direction TB
        Uploader[File Uploader]
        Preview[Data Preview Table]
        Controls[Sort/Clean/Filter Controls]
        RecipeUI[Recipe Manager UI]
        Exporter[Export Button]
        AuditUI[Audit Log Viewer]
    end

    %% Service Layer
    subgraph Services [Streamlit Services]
        direction TB
        UploadSvc[upload_service.py]
        SchemaSvc[schema_detection.py]
        CleanSvc[data_cleaning.py]
        SortSvc[sorting.py]
        FilterSvc[filtering.py]
        DedupSvc[deduplication.py]
        SplitSvc[splitting.py]
        RecipeSvc[recipe_service.py]
        AuditSvc[audit_service.py]
        ExportSvc[export_service.py]
    end

    %% Data Layer
    subgraph Data [Processing Engine]
        direction TB
        DataEngine[pandas DataFrame Engine]
    end

    %% Storage Layer
    subgraph Storage [SQLite Database]
        direction TB
        Recipes[recipes Table]
        AuditLogs[audit_logs Table]
        Metadata[column_metadata Table]
    end

    %% Connections
    Uploader -->|upload file| UploadSvc
    UploadSvc -->|passes to| DataEngine
    DataEngine -->|transforms| Services
    Services -->|saves/loads| Storage
    RecipeSvc -->|applies| DataEngine
    ExportSvc -->|generates| .xlsx file
    ExportSvc -->|writes audit entry| Storage
    AuditUI -->|reads| Storage
    RecipeUI -->|loads/saves| Storage

    style UI fill:#f0f8ff,stroke:#3366bb,stroke-width:2px
    style Services fill:#e8f5e9,stroke:#3366bb,stroke-width:2px
    style Data fill:#fff3e0,stroke:#3366bb,stroke-width:2px
    style Storage fill:#f3e5f5,stroke:#3366bb,stroke-width:2px
```

### Diagram Description
- **Browser / Streamlit Frontend**: User interacts with file uploader, preview, controls, recipe manager, export button, and audit log viewer.
- **Streamlit Services**: Each processing step (upload, schema detection, cleaning, sorting, filtering, deduplication, splitting, recipe management, audit, export) lives in its own service module.
- **Processing Engine**: A single pandas DataFrame flows through the services; never written to disk until export.
- **SQLite Database**: Persists recipes, audit logs, and column metadata across sessions.
- **Exported .xlsx**: Final output with data + Summary sheet; formatting preserved via openpyxl.

---

## 3. Project Folder Structure

```
sheetSort/
├── app/
│   ├── main.py                  # Streamlit entry point; page routing
│   ├── ui/
│   │   ├── components.py        # Reusable UI components (cards, tables, etc.)
│   │   └── pages/
│   │       ├── upload.py        # File upload + preview page
│   │       ├── process.py       # Sorting/cleaning/filtering/splitting UI
│   │   ├── services/
│   │   │   ├── upload_service.py      # Validate, save temp, pass to engine
│   │   │   ├── schema_detection.py    # Auto‑detect header, column types
│   │   │   ├── data_cleaning.py       # Trim, standardize, flag invalid
│   │   │   ├── sorting.py              # Multi‑column sort, custom order
│   │   │   ├── filtering.py             # Text/numeric/date filters, AND/OR
│   │   │   ├── deduplication.py        # Exact + near‑duplicate removal
│   │   │   ├── splitting.py             # Split by selected column into sheets
│   │   │   ├── recipe_service.py        # Save/load/update/delete/apply recipes
│   │   │   └── audit_service.py         # Write/read audit log entries
│   │   ├── processors/
│   │   │   └── processing_pipeline.py # Orchestrates the pipeline steps
│   │   ├── models/
│   │   │   ├── data_models.py          # Pydantic / typed dicts for core models
│   │   │   └── recipe_models.py        # Recipe, SortRule, FilterRule, etc.
│   │   └── utils/
│   │       ├── config.py               # Upload limits, allowed types, paths
│   │       ├── logger.py               # App‑wide logging config
│   │       └── exceptions.py           # Custom exception hierarchy
│   └── __init__.py
├── tests/
│   ├── test_upload.py
│   ├── test_schema.py
│   ├── test_cleaning.py
│   ├── test_sorting.py
│   ├── test_filtering.py
│   ├── test_dedup.py
│   ├── test_splitting.py
│   ├── test_export.py
│   └── test_recipes.py
├── sample_data/
│   ├── exam_roster.xlsx              # Real‑looking college data (anonymized)
│   ├── placement_data.csv
│   └── attendance_sample.csv
├── requirements.txt                  # Pinned dependencies
├── Dockerfile                        # Docker build config
├── .env.example                      # env vars with defaults
├── README.md                         # Setup + run instructions
└── .gitignore
```

### Folder Rationale
- **app/**: All code lives here; keeps the root clean.
- **app/ui/pages/**: Streamlit's default page routing; each page is a self‑contained module.
- **app/services/**: Business‑logic separation; UI calls services, not raw pandas calls.
- **app/processors/**: Pipeline orchestration; individual steps can be re‑ordered or disabled.
- **app/models/**: Typed data models for type‑hinting and documentation.
- **app/utils/**: Configuration, logging, error helpers — used across modules.
- **tests/**: pytest‑discovered test files; one per feature area.
- **sample_data/**: Anonymized college data for demos and testing.
- **requirements.txt / Dockerfile / README.md**: Standard deployment artifacts.

---

## 4. Core Data Models

Models are defined as **Python typed dicts** (or Pydantic v2 if added later) for clarity, type‑hinting, and documentation. No external database schema migration needed at MVP — SQLite handles it.

### 4.1 `uploaded_file.py` — Metadata about an uploaded file

```python
from __future__ import annotations
from datetime import datetime
from typing import Dict, List, Optional, Literal

UploadedFile = Dict[str, object]
"""
Key            | Type                    | Description
---------------|-------------------------|------------------------------------------
file_id        | str                     # Unique UUID for this upload
original_name  | str                     # User‑supplied filename
upload_ts      | datetime                # When the file was uploaded
row_count      | int                     # Total rows (incl. header)
col_count      | int                     # Total columns
file_type      | Literal['xlsx', 'xls', 'csv']  # Detected type
temp_path      | str                     # Path to temp copy (read‑only, deleted after export)
status         | Literal['pending', 'processed', 'error']  # Processing state
error_message  | Optional[str]         # If status == 'error'
"""

```

### 4.2 `column_metadata.py` — Detected info per column

```python
ColumnType = Literal['text', 'number', 'date', 'email', 'phone', 'id']

ColumnMetadata = Dict[str, object]
"""
Key            | Type                    | Description
---------------|-------------------------|------------------------------------------
column_name    | str                     # As detected (may be normalized)
column_index   | int                     # 0‑based position in data
data_type      | ColumnType              # Auto‑detected type
sample_values  | List[object]            # First 5 non‑null values for user review
is_header      | bool                    # Is this the header row?
normalized_name| str                     # Cleaned version (trimmed, lowercase, underscores)
"""

```

### 4.3 `sort_rule.py` — Sorting specification

```python
from __future__ import annotations
from typing import Literal

SortRule = Dict[str, object]
"""
Rule for ordering the DataFrame.

Key           | Type                    | Description
--------------|-------------------------|------------------------------------------
column_name   | str                     # Name of column to sort by
order         | Literal['asc', 'desc']  # Ascending or descending
custom_order  | Optional[List[str]]   # e.g., ['CSE', 'IT', 'ECE', 'Mechanical']
priority      | int                     # 0 = primary, 1 = secondary, etc.
"""

```

### 4.4 `filter_rule.py` — Filter specification

```python
from __future__ import annotations
from typing import Literal, Optional

FilterCondition = Literal['contains', 'exact', 'gt', 'gte', 'lt', 'lte', 'between', 'date_range']

FilterRule = Dict[str, object]
"""
Rule for filtering rows.

Key           | Type                    | Description
--------------|-------------------------|------------------------------------------
column_name   | str                     # Column to filter on
condition     | FilterCondition         # Type of comparison
value         | object                  # Depends on condition (e.g., number, date string, text)
value2        | Optional[object]      # For 'between' / 'date_range'
logic         | Literal['and', 'or']  # How this combines with other filters
"""

```

### 4.5 `cleaning_rule.py` — Cleaning operation specification

```python
from __future__ import annotations
from typing import Literal

CleaningOperation = Literal[
    'trim_spaces',
    'remove_empty_rows',
    'remove_empty_cols',
    'standardize_headers',
    'date_to_ddmmyyyy',
    'normalize_phone',
    'validate_email',
    'flag_invalid',
]

CleaningRule = Dict[str, object]
"""
Rule describing a single cleaning step.

Key           | Type                    | Description
--------------|-------------------------|------------------------------------------
operation     | CleaningOperation       # What to do
enabled       | bool                    # User toggle on/off
target_columns| Optional[List[str]]     # Columns to apply to (None = all)
"""

```

### 4.6 `split_rule.py` — Split specification

```python
from __future__ import annotations
from typing import Literal

SplitRule = Dict[str, object]
"""
Rule for splitting data into separate sheets.

Key           | Type                    | Description
--------------|-------------------------|------------------------------------------
by_column     | str                     # Column name to split on
sheet_name_prefix | str                 # Prefix for generated sheet names (e.g., "Dept_")
include_header| bool                    # Whether each sheet keeps the header row
"""

```

### 4.7 `recipe.py` — Saved workflow

```python
from __future__ import annotations
from datetime import datetime
from typing import List, Dict, Optional
from .models.sort_rule import SortRule
from .models.filter_rule import FilterRule
from .models.cleaning_rule import CleaningRule
from .models.split_rule import SplitRule

Recipe = Dict[str, object]
"""
A reusable processing workflow.

Key           | Type                    | Description
--------------|-------------------------|------------------------------------------
recipe_id     | str                     # UUID
name          | str                     # User‑given name (e.g., "Exam Report")
created_ts    | datetime                # When the recipe was saved
sort_rules    | List[SortRule]          # May be empty
filter_rules  | List[FilterRule]        # May be empty
cleaning_rules| List[CleaningRule]      # May be empty
split_rule    | Optional[SplitRule]    # May be None
description   | Optional[str]          # Free‑form note
is_active     | bool                    # Whether this is the active recipe
"""

```

### 4.8 `processing_result.py` — Outcome of a file‑processing run

```python
from __future__ import annotations
from datetime import datetime
from typing import Dict, List, Optional

ProcessingResult = Dict[str, object]
"""
Result returned after a full pipeline run.

Key           | Type                    | Description
--------------|-------------------------|------------------------------------------
output_path   | str                     # Path to exported .xlsx (None if cancelled)
summary       | Dict[str, object]      # See summary schema below
audit_entry_id| str                     # ID of the audit log row
status        | Literal['success', 'partial', 'failed']
"""

Summary = Dict[str, object]
"""
Key           | Type                    | Description
--------------|-------------------------|------------------------------------------
original_rows | int                     # Before processing
final_rows    | int                     # After all operations
duplicates_removed | int             # Exact + near‑duplicate count
blank_rows_removed | int             # Empty‑row count
invalid_values_flagged | int           # How many cells/rows flagged
columns_modified | int                 # How many columns had changes applied
processed_ts  | datetime                # When processing completed
"""

```

### 4.9 `audit_log_entry.py` — Audit‑log row

```python
from __future__ import annotations
from datetime import datetime
from typing import Literal

AuditLogEntry = Dict[str, object]
"""
A single row in the audit log SQLite table.

Key           | Type                    | Description
--------------|-------------------------|------------------------------------------
entry_id      | str                     # UUID (primary key)
user_action   | Literal['upload', 'process', 'recipe_save', 'recipe_load', 'recipe_delete', 'export']  # What happened
file_id       | Optional[str]          # UUID of the uploaded file (if applicable)
recipe_id     | Optional[str]          # UUID of the recipe used (if applicable)
timestamp     | datetime                # When the action occurred
rows_processed| int                     # How many rows were in the input
rows_exported | int                     # How many rows made it to the output
notes         | Optional[str]          # Free‑form notes (e.g., error type)
"""

```

---

## 5. Processing Pipeline (Defined Sequence)

```
Upload → Validate → Detect Schema → Clean → Sort → Filter → Deduplicate → Split → Summarize → Export
```

### Pipeline Steps (with service responsibility)

| Step | Service | Key Actions |
|------|---------|-------------|
| **1. Upload** | `upload_service.py` | Accept file, validate type/size, save temporary read‑only copy, create `UploadedFile` metadata, display preview |
| **2. Validate** | `upload_service.py` | Check file not empty, header detectable, no corrupt‑Excel errors; return user‑friendly messages |
| **3. Detect Schema** | `schema_detection.py` | Auto‑detect header row; infer column data types (text/number/date/email/phone/id); present to user for override |
| **4. Clean** | `data_cleaning.py` | Apply user‑selected cleaning operations (trim, remove empty rows/cols, standardize headers, date/phone/email normalization, flag invalid values) |
| **5. Sort** | `sorting.py` | Apply multi‑column sort with priority, ascending/descending, custom order (e.g., Department: CSE, IT, ECE, Mechanical) |
| **6. Filter** | `filtering.py` | Apply text contains/exact match, numeric range, date range filters; support AND/OR logic between multiple filters |
| **7. Deduplicate** | `deduplication.py` | Remove exact duplicates; optionally detect near‑duplicates on selected columns; show preview before removal; let user keep first/last/review manually |
| **8. Split** | `splitting.py` | Split data into separate sheets by selected column (Department, Year, Batch, Course, Status); generate sheet names automatically |
| **9. Summarize** | `processing_pipeline.py` | Compute summary stats: original count, final count, duplicates removed, blank rows removed, invalid values flagged, columns modified, timestamp |
| **10. Export** | `export_service.py` | Write cleaned DataFrame + Summary sheet to .xlsx with formatting (bold headers, frozen header row, auto column width, filters enabled); write audit log entry |

### Pipeline Orchestration

- **`processing_pipeline.py`** coordinates the steps; each step receives the current DataFrame and returns the transformed DataFrame plus any metadata needed for the next step.
- Steps are **modular**: any step can be skipped or reordered by the user via the UI.
- **Error propagation**: if a step fails, the pipeline stops, an error message is shown, and no export occurs.
- **Recipe application**: when a user loads a Recipe, the stored sort/clean/filter/split rules are injected as the first pipeline steps.

---

## 6. Error‑Handling Rules

| Error Scenario | Handling Approach | User Message |
|----------------|-------------------|--------------|
| **E‑1 Empty file** | Detect 0‑byte upload before processing; show inline warning. | "The file is empty. Please upload a file with data." |
| **E‑2 No detectable header** | Scan first row; if all values are null or look like data, prompt user to select header row. | "Could not detect a header row. Please confirm which row contains column names." |
| **E‑3 Unsupported file type** | Check extension against `ALLOWED_EXTENSIONS` in config; reject early. | "Unsupported file type. Please upload .xlsx, .xls, or .csv." |
| **E‑4 Corrupted Excel file** | Wrap `openpyxl.load_workbook` in `try/except`; fall back to reading CSV if applicable; show generic error. | "Could not read the Excel file. It may be corrupted. Try uploading a CSV instead." |
| **E‑5 Missing selected column** | When user selects a column that doesn't exist (e.g., after renaming), highlight the issue. | "The selected column 'X' was not found. Please check the column names." |
| **E‑6 Invalid date format** | During cleaning, attempt conversion; unparseable dates are flagged, not silently dropped. | "Some dates could not be parsed (DD‑MM‑YYYY). They have been flagged for review." |
| **E‑7 File too large** | Configurable max rows/bytes (e.g., 100K rows / 50 MB). Enforce before processing; show progress for large files. | "File exceeds the size limit (100 K rows / 50 MB). Please split the file and upload again." |
| **E‑8 Duplicate column names** | Auto‑rename with suffixes (_1, _2); allow user to override. | "Duplicate column names detected. They have been auto‑renamed to Column_1, Column_2. You can rename them manually." |
| **E‑9 Invalid email/phone in data** | Validate format; flag rows/cells without removing them; show count in summary. | "X invalid email(s)/Y invalid phone number(s) found. Review the flagged rows." |
| **E‑10 Audit‑log write failure** | Atomic SQLite transaction; if write fails, log to stderr and show non‑critical banner. | "Could not record audit entry. Processing completed; admin will review." |

### Global Error‑Handling Pattern (in `app/utils/exceptions.py`)

```python
class SheetSortError(Exception):
    """Base exception for all SheetSort‑specific errors."""
    status_code: int = 400  # HTTP‑style; used by Streamlit error banners
    user_message: str = "An error occurred. Please try again."
    log_message: str = "Unknown error"

    def __init__(self, user_message: str | None = None, log_message: str | None = None):
        self.user_message = user_message or self.user_message
        self.log_message = log_message or self.log_message
        super().__init__(self.user_message)


class InvalidFileError(SheetSortError):
    """Raised when the uploaded file cannot be processed."""
    status_code = 400
    user_message = "The uploaded file could not be processed. Please check the format and try again."
```

All service functions raise `SheetSortError` (or subclasses); the UI catches them and displays `user_message` via `st.error()`. The `log_message` is written to the app’s logger and eventually to the audit log if appropriate.

---

## 7. Security and Privacy Considerations

| Area | Recommendation | Rationale |
|------|----------------|-----------|
| **Data minimization** | Never store the original uploaded file permanently. Write to a temporary path; delete after export or after 24 h if not exported. | Reduces exposure of sensitive student data. |
| **In‑memory processing** | Perform all data manipulation (pandas operations) in memory; only write the final .xlsx to disk. | Limits data residency time. |
| **SQLite access** | The SQLite database is file‑based and local. Set file permissions (read/write only to the app process). | Prevents unauthorized reading of recipes/audit logs. |
| **No external APIs** | The MVP uses no third‑party AI/ML APIs; all processing is local. | Avoids sending college data outside the premises. |
| **User session isolation** | If multi‑user deployment is later needed, each user’s SQLite DB, recipes, and audit log are namespaced by user ID. | Prevents cross‑user data leakage. |
| **Audit log** | Records user action, file name, recipe used, timestamp, rows processed, export event. **Does NOT** store raw file contents — only metadata. | Provides accountability without exposing PII. |
| **Anonymization option** | Offer a checkbox in the UI: "Use anonymized data (remove roll numbers, emails)" for evaluation/development. | Supports pilot use with sample data. |
| **HTTPS for local deployments** | If the app is accessed via a intranet, enforce HTTPS (via reverse proxy like Nginx). | Encrypts data in transit within the college network. |
| **Backup & restore** | Provide a UI button to export the SQLite DB (recipes + audit log) and a separate restore flow. | Enables disaster recovery without data loss. |

---

## 8. Summary of Stage 1 Deliverables

| Deliverable | Status |
|-------------|--------|
| **Technology stack recommendation** | ✅ Python 3.11+, Streamlit, pandas, openpyxl, SQLite, pytest, Docker |
| **Mermaid architecture diagram** | ✅ Shown above with component description |
| **Folder structure** | ✅ Detailed layout with rationale |
| **Core data models** | ✅ 9 model definitions (UploadedFile, ColumnMetadata, SortRule, FilterRule, CleaningRule, SplitRule, Recipe, ProcessingResult, AuditLogEntry) |
| **Processing pipeline** | ✅ 10‑step sequence from Upload → Export, with service responsibilities |
| **Error‑handling rules** | ✅ 10 error scenarios with handling approach + user messages; global exception pattern |
| **Security & privacy considerations** | ✅ 7 recommendations covering data minimization, in‑memory processing, SQLite access, no external APIs, audit log, anonymization, HTTPS, backup/restore |

---

**Stage 1 is now complete.** The next step is **Stage 2 — MVP Implementation**, which will build the actual runnable SheetSort application with all the features listed in the MVP feature list (file upload, schema detection, sorting, cleaning, duplicate handling, filtering, splitting, export with summary sheet, recipes, audit log).

**Please approve proceeding to Stage 2**, and I will begin coding the MVP.