# Security Policy

## Overview

SheetSort is designed with a **privacy-first, zero-cloud architecture**. All spreadsheet ingestion, cleaning, deduplication, sorting, filtering, splitting, and exporting operations run entirely within the local host's memory and process boundary. No student, faculty, or institutional records are transmitted across the internet.

---

## Supported Versions

| Version | Supported | Security Updates |
|---|---|---|
| **v1.0.0** | :white_check_mark: | Full Active Support |
| < v1.0.0 | :x: | Deprecated / Development |

---

## Security Architecture & Defense Layers

The codebase has undergone a penetration test and source code audit. The following defensive controls are active:

### 1. CSV / Spreadsheet Formula Injection (CSV Injection)
- **Threat:** Malicious spreadsheet entries starting with formula operators (`=`, `+`, `-`, `@`) executing arbitrary system commands via DDE or macros when opened by Excel.
- **Defense:** `sheetsort/app/services/export_service.py` runs `safe_excel_value()` across every cell, automatically prepending a single quote (`'`) to neutralize formula execution while preserving display readability.

### 2. Regular Expression Denial of Service (ReDoS)
- **Threat:** User-supplied search queries in text containment filters containing evil regular expressions (e.g. `(a+)+$`) freezing server worker threads.
- **Defense:** Enforced literal substring matching (`regex=False`) in `sheetsort/app/services/filtering.py`. Regex engines are never invoked on user-supplied strings.

### 3. Magic-Byte File Signature Verification
- **Threat:** Disguised executables or malicious binaries uploaded with permitted extensions (`.xlsx`, `.xls`, `.csv`).
- **Defense:** `sheetsort/app/services/upload_service.py` inspects file binary headers:
  - `.xlsx`: Validated against ZIP signature `b"PK\x03\x04"`.
  - `.xls`: Validated against OLE2 compound document header `b"\xd0\xcf\x11\xe0"`.
  - `.csv`: Validated against UTF-8 and Latin-1 character streams.

### 4. Path-Traversal & Database Containment
- **Threat:** Manipulating `SHEETSORT_RECIPE_DB` to read or overwrite arbitrary operating system databases.
- **Defense:** `get_safe_db_path()` validates that database targets resolve exclusively inside approved user directories (`~/SheetSort/` or the project root).

### 5. Localhost Network Isolation
- **Threat:** Network snooping of confidential college records over local campus LAN or Wi-Fi.
- **Defense:** The desktop launcher strictly binds to `127.0.0.1` (loopback only) and disables browser analytics telemetry.

---

## Reporting a Vulnerability

If you discover a security vulnerability within SheetSort, please report it responsibly:

1. **Do NOT open a public GitHub issue.**
2. Send an email to the maintainer: **sunilsawant6812@gmail.com** with the subject:
   `[SECURITY] SheetSort Vulnerability Report - <Brief Summary>`
3. Include:
   - Description of the vulnerability
   - Steps or proof-of-concept (PoC) file to reproduce
   - Potential impact
4. You will receive an acknowledgment within **48 hours**, followed by a triage assessment and remediation timeline.

