# 📊 SheetSort — College Data Processing & Excel Automation

[![Release](https://img.shields.io/badge/Release-v1.0.0-blue.svg)](https://github.com/saish-vc/excel-sorter/releases/tag/v1.0.0)
[![CI](https://github.com/saish-vc/excel-sorter/actions/workflows/ci.yml/badge.svg)](https://github.com/saish-vc/excel-sorter/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.12%2B-brightgreen.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Tests-63%20Passing-success.svg)](https://github.com/saish-vc/excel-sorter)
[![Security Audited](https://img.shields.io/badge/Security-Pentested%20%26%20Hardened-blueviolet.svg)](SECURITY.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**SheetSort** is an intelligent, air-gapped desktop application engineered for college administrative offices, examination cells, training & placement (T&P) cells, and departmental staff to clean, standardize, filter, split, and export complex Excel and CSV datasets in seconds.

---

## 🚀 App v1 Download Link

### [📥 Click Here to Download SheetSort v1.0.0 for Windows (64-bit)](https://github.com/saish-vc/excel-sorter/releases/download/v1.0.0/SheetSort-v1.0.0-windows-x64.zip)

> 💡 **Release Hub:** [View Release Notes & Assets on GitHub](https://github.com/saish-vc/excel-sorter/releases/tag/v1.0.0)

### Quick Run Instructions
1. Download `SheetSort-v1.0.0-windows-x64.zip` from the link above.
2. Right-click and choose **Extract All...**.
3. Open the folder and double-click **`SheetSort.exe`**.
4. The application opens directly in your default browser at `http://127.0.0.1:8501`. No Python installation, drivers, or terminal required!

---

## 📚 Complete Project Documentation

| Document | Purpose & Audience |
|---|---|
| **[📄 2-Page Project Synopsis (Printable HTML)](docs/SheetSort_Project_Synopsis.html)** | Exact 2-page A4 document ready to print (<kbd>Ctrl</kbd>+<kbd>P</kbd>) for college submissions, project vivas, and accreditation. |
| **[🎓 College Sales Pitch & Demo Script](docs/COLLEGE_SALES_PITCH.md)** | Executive proposal letter, 5-minute live demo script, objection handling cheat sheet, and pricing models for pitching to colleges. |
| **[📖 Administrative Staff User Manual](docs/USER_GUIDE.md)** | Step-by-step visual guide covering all 9 application modules for non-technical college staff. |
| **[🔒 Security Policy & Audit Certification](SECURITY.md)** | Detailed documentation of the 8 patched vulnerability vectors (Formula Injection, ReDoS, magic-bytes, etc.). |
| **[📋 Changelog](CHANGELOG.md)** | Release history, feature additions, and security patch breakdown for v1.0.0. |
| **[🛠️ Contributing Guidelines](CONTRIBUTING.md)** | Development environment setup, coding conventions, and test execution instructions. |

---

## 🔄 End-to-End Processing Architecture

```text
  [ Raw Spreadsheet (.xlsx / .xls / .csv) ]
                     │
                     ▼
  ┌──────────────────────────────────────────────┐
  │ 1. Ingestion & Magic-Byte Validation         │
  │    (Blocks disguised malware & checks caps)  │
  └──────────────────┬───────────────────────────┘
                     ▼
  ┌──────────────────────────────────────────────┐
  │ 2. Heuristic Schema & Header Detection       │
  │    (Bypasses college banners, infers types)  │
  └──────────────────┬───────────────────────────┘
                     ▼
  ┌──────────────────────────────────────────────┐
  │ 3. Automated Data Cleaning & Standardization │
  │    (Trim whitespace, DD-MM-YYYY, phones)     │
  └──────────────────┬───────────────────────────┘
                     ▼
  ┌──────────────────────────────────────────────┐
  │ 4. Sorting, Filtering & Deduplication        │
  │    (Branch priority, boolean logic, fuzzy)   │
  └──────────────────┬───────────────────────────┘
                     ▼
  ┌──────────────────────────────────────────────┐
  │ 5. Departmental Workbook Splitting           │
  │    (Auto-creates sub-sheets per department)  │
  └──────────────────┬───────────────────────────┘
                     ▼
  ┌──────────────────────────────────────────────┐
  │ 6. Formatted OpenPyXL Export + Summary Tab   │
  │    (AutoFilter, frozen rows, formula safety) │
  └──────────────────┬───────────────────────────┘
                     ▼
  ┌──────────────────────────────────────────────┐
  │ 7. Relational Recipe & SQLite Audit Logging  │
  │    (1-Click replay for next semester)        │
  └──────────────────────────────────────────────┘
```

---

## ✨ Core Capabilities Built for Colleges

- **Autonomous Header Detection:** Bypasses 1 to 4 messy college banner rows (e.g. *"Semester VII University Examinations"*) and automatically identifies true column headers.
- **Academic Sorting & Custom Branch Priority:** Sort by branch priority order (e.g., `CSE > IT > ECE > Mechanical > Civil`) or student merit rank.
- **Departmental Sheet Splitting:** Divides a master file of 5,000+ students into department-wise tabs in a single workbook with one click.
- **1-Click Recipe Engine:** Save routine semester workflows as a named "Recipe" and re-apply them to subsequent exam/attendance files instantly.
- **Audit Compliance Trail:** Complete SQLite audit logging of rows processed, modifications, and user actions for NAAC, NBA, and NIRF audits.
- **100% Student Data Privacy:** Operates entirely within your local machine's memory without cloud transmission.

---

## 🧪 Testing with Included College Datasets

The repository includes three realistic sample datasets in [`sheetsort/sample_data/`](sheetsort/sample_data/) to test or demonstrate the application immediately:

1. **`exam_roster.xlsx`**: Exam marks across 6 engineering departments with mixed dates and student roll numbers.
2. **`attendance_sample.csv`**: Attendance percentages and risk categories across 200 students to test defaulter filtering (<75%).
3. **`placement_data.csv`**: Campus placement records with multiple company offers, salary tiers (LPA), and duplicate student applicants.

---

## 💻 Running from Source (Development)

```bash
# 1. Clone the repository
git clone https://github.com/saish-vc/excel-sorter.git
cd excel-sorter

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the automated test suite
python -m pytest sheetsort/tests/ -v

# 4. Launch the application
streamlit run sheetsort/app/main.py
```

---

## 📦 Standalone Windows Executable Build

To compile a standalone Windows `.exe` using PyInstaller:
```powershell
powershell -ExecutionPolicy Bypass -File .\build_windows.ps1
```
The distribution bundle will be generated in `dist\SheetSort\`.

---

## 📄 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
