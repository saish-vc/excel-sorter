# Changelog

All notable changes to **SheetSort** are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [v1.0.0] - 2026-11-01

### 🎉 Initial Production Release

#### Added
- **Core Processing Pipeline:**
  - File upload engine supporting `.xlsx`, `.xls`, and `.csv` files up to 50 MB and 100,000 rows.
  - Heuristic header row detection scanning top 5 rows for text density to ignore banner/title rows.
  - Automatic column data type inference: ID, Date, Email, Phone, Number, and Text with user override capability.
  - 8 Vectorized cleaning operations: whitespace trimming, header standardization (`snake_case`), date formatting to `DD-MM-YYYY`, phone normalization, email validation, and invalid value tagging.
  - Multi-level priority sorting supporting both ascending/descending and custom academic categorical orders (e.g. `CSE, IT, ECE, Mechanical`).
  - Compound Boolean filtering (`AND` / `OR` logic) supporting exact match, substring containment, numeric ranges (`gt`, `gte`, `lt`, `lte`, `between`), and date ranges.
  - Dual-mode deduplication: exact row deduplication (keep-first / keep-last) and fuzzy near-duplicate matching with similarity threshold.
  - Departmental splitting engine dividing master rosters into dedicated sub-sheets with sanitized 31-character Excel sheet names.
  - Formatted OpenPyXL export: bold frozen header rows, AutoFilter enablement, auto-fitted column dimensions, and executive processing Summary sheet.
  - Recipe Engine: Save, load, update, delete, and 1-click re-apply complex multi-step workflows stored in an SQLite relational database.
  - SQLite Audit Trail logging every file upload, recipe execution, rows processed, and export timestamps.

- **Standalone Windows Distribution:**
  - Standalone 64-bit Windows executable bundle (`dist/SheetSort/SheetSort.exe`).
  - Automated PowerShell packaging script (`build_windows.ps1`).
  - GitHub Actions automated release pipeline (`.github/workflows/release.yml`).

- **Security & Pentesting Patches:**
  - **Patched ReDoS Vulnerability:** Added `regex=False` to `str.contains()` preventing algorithmic complexity attacks.
  - **Patched File Spoofing:** Added magic-byte inspection for `.xlsx` (ZIP `PK\x03\x04`), `.xls` (OLE2 `\xd0\xcf\x11\xe0`), and text streams.
  - **Patched CSV Formula Injection:** Added automatic prepending of single quote (`'`) to cell strings beginning with `=`, `+`, `-`, or `@`.
  - **Patched Database Path Traversal:** Added `get_safe_db_path()` confining SQLite writes to verified local directories.
  - **Patched Information Leaks:** Sanitized upload error strings to prevent leaking filesystem directories.
  - **Patched Audit Log Crash:** Handled SQLite ISO string formatting safely to prevent runtime exceptions.
  - **Patched Recipe Input Flooding:** Implemented name (200 char) and description (2000 char) bounds in `save_recipe()`.

- **Testing & Verification:**
  - Pytest test suite expanded from 57 to **63 unit tests** passing with 100% success rate.
  - Added dedicated security test suites: `TestFileContentValidation` and `TestFilteringSecurity`.

- **Documentation & College Pitch Pack:**
  - Complete 2-page printable Project Synopsis (`docs/SheetSort_Project_Synopsis.html` and `.md`).
  - Institutional Sales Pitch & Demo Script (`docs/COLLEGE_SALES_PITCH.md`).
  - Administrative Staff User Manual (`docs/USER_GUIDE.md`).
  - Security Policy (`SECURITY.md`) and Contributing Guidelines (`CONTRIBUTING.md`).

