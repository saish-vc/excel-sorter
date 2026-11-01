# 📊 SheetSort — College Data Processing & Excel Automation

[![Version](https://img.shields.io/badge/Release-v1.0.0-blue.svg)](https://github.com/saish-vc/excel-sorter/releases/tag/v1.0.0)
[![Python](https://img.shields.io/badge/Python-3.12%2B-brightgreen.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Tests-63%20Passing-success.svg)](https://github.com/saish-vc/excel-sorter)
[![Security Audited](https://img.shields.io/badge/Security-Audited%20%26%20Patched-blueviolet.svg)](https://github.com/saish-vc/excel-sorter)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11%20%28x64%29-orange.svg)](https://github.com/saish-vc/excel-sorter/releases)

**SheetSort** is an intelligent, privacy-preserving desktop application built for college administrative offices, exam cells, training & placement cells, and departmental staff to clean, standardize, filter, split, and export complex Excel and CSV datasets in seconds.

---

## 🚀 App v1 Download Link

### [📥 Click Here to Download SheetSort v1.0.0 for Windows (64-bit)](https://github.com/saish-vc/excel-sorter/releases/download/v1.0.0/SheetSort-v1.0.0-windows-x64.zip)

> 💡 **Release Page:** [View Release Notes & Assets on GitHub](https://github.com/saish-vc/excel-sorter/releases/tag/v1.0.0)

### Quick Run Instructions
1. Download `SheetSort-v1.0.0-windows-x64.zip` from the link above.
2. Right-click and choose **Extract All...**.
3. Open the folder and double-click **`SheetSort.exe`**.
4. The application opens directly in your default browser at `http://127.0.0.1:8501`. No Python installation or command prompt required!

---

## ✨ Key Features Built for Colleges

| Feature | Description |
|---|---|
| **📁 Smart File Upload** | Accepts `.xlsx`, `.xls`, and `.csv` files up to 50 MB / 100,000 rows. Includes magic-byte verification to reject corrupted or spoofed files. |
| **🔍 Auto Schema Detection** | Automatically detects messy header rows (e.g. college banners/metadata on lines 1–3) and infers data types (Roll No, Email, Phone, Marks, Dates). |
| **🧹 1-Click Data Cleaning** | Trims stray whitespace, strips empty rows/columns, standardizes headers to `snake_case`, normalizes 10-digit phone numbers, converts dates to `DD-MM-YYYY`, and flags invalid emails. |
| **📊 Multi-Column Sorting** | Multi-level sorting with **custom academic priority** (e.g. `CSE, IT, ECE, Mechanical, Civil`) or merit ranking. |
| **🎯 Advanced Filtering** | Filter by text containment, exact matching, score thresholds (`>= 75`), or date ranges with `AND` / `OR` logic. |
| **🗑️ Deduplication** | Removes exact student duplicates or flags near-duplicates using configurable fuzzy similarity matching. |
| **✂️ Departmental Splitting** | Splits a single master sheet into multiple dedicated sheets (e.g., one sheet per department or semester) inside a single workbook. |
| **⚡ Recipe Workflow Engine** | Save multi-step processing workflows as named "Recipes" (e.g. *"Exam Roster Cleaner"*, *"Placement Data Formatter"*) and re-apply them to new files in 1 click. |
| **📤 Professional Excel Export** | Generates formatted Excel spreadsheets with bold frozen headers, auto-adjusted column widths, active auto-filters, and an executive **Summary tab**. |
| **📋 Audit Log** | Built-in SQLite audit trail recording all user actions, rows processed, exports, and timestamps. |

---

## 🔒 Enterprise-Grade Security

The application has been pentested and audited for enterprise deployment in educational institutions:

- **Formula Injection Prevention (CSV/Excel Injection)**: Automatically neutralizes unsafe formula characters (`=`, `+`, `-`, `@`) in export cells to prevent spreadsheet macro execution.
- **ReDoS Protection**: Search and text-filtering use strict literal string matching (`regex=False`), neutralizing Regular Expression Denial of Service attacks.
- **Magic-Byte Content Validation**: Verifies genuine file signatures (`PK` for `.xlsx`, OLE2 for `.xls`) to block disguised malicious executables.
- **Path-Traversal Guard**: SQLite database paths are strictly constrained to user-approved application directories.
- **Isolated Localhost Binding**: Desktop runner binds strictly to `127.0.0.1`—no network exposure or external data telemetry.
- **Privacy First**: All data processing runs entirely on the local machine. Zero student records are uploaded to cloud servers.

---

## 💻 Running from Source (Development)

### Prerequisites
- Python 3.12 or higher
- Git

### Setup
```bash
# 1. Clone the repository
git clone https://github.com/saish-vc/excel-sorter.git
cd excel-sorter

# 2. Install dependencies
pip install -r requirements.txt
# (or pip install streamlit pandas openpyxl)

# 3. Launch the web application
streamlit run sheetsort/app/main.py
```

### Running the Test Suite
```bash
python -m pytest sheetsort/tests/ -v
# 63 tests passing
```

---

## 📦 Building the Windows Executable
To package the standalone Windows binary:
```powershell
.\build_windows.ps1
```
The standalone executable bundle will be generated in `dist\SheetSort\`.

---

## 📄 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
