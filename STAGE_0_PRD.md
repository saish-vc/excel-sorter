# SheetSort - Stage 0: Product Discovery and Requirements

**Status:** Awaiting approval to begin Stage 1  
**Last updated:** 30 October 2026

## 1. Product Requirements Document

### Product summary

SheetSort is a web application that helps college administrative departments turn imperfect Excel and CSV files into clean, standardized, sorted, filtered, and export-ready Excel reports. A staff member uploads a file, configures or loads a reusable workflow (a **Recipe**), reviews the result, and downloads a new report. The source file is never edited or overwritten.

### Users

- College administrative staff
- Exam Cell coordinators
- Placement officers
- Attendance officers
- Department heads and college administrators

### Problem

Administrative teams repeatedly clean data by hand: deleting blank rows, correcting headers, sorting inconsistent values, finding duplicates, applying filters, and creating separate department reports. This is slow, difficult to repeat consistently, and prone to accidental changes to the original file.

### Value proposition

**Upload a messy file, apply a saved workflow, and download a clean, standardized report in minutes.**

### Goals

1. Make routine college-report preparation achievable by a non-technical staff member without formulas or scripts.
2. Make repeatable processes reusable through named Recipes.
3. Preserve data integrity with previews, explicit actions, summaries, and audit events.
4. Support both local and college-server deployment without sending student data to third parties.

### Non-goals

- Replacing Microsoft Excel, Google Sheets, or a college ERP/SIS.
- Collaborative spreadsheet editing, formula authoring, or general workbook design.
- Grade calculation, attendance capture, admissions processing, or ERP master-data management.
- Automatic deletion or correction of ambiguous records without the user's chosen rule.

### Functional requirements

| ID | Requirement |
|---|---|
| FR-01 | Upload `.xlsx`, `.xls`, and `.csv` files; validate extension, size, and readability. |
| FR-02 | Detect a likely header row; preview parsed data and let the user recover from blank, duplicate, or inconsistent headers. |
| FR-03 | Display upload metadata: filename, row count, column count, and timestamp. |
| FR-04 | Infer text, number, date, email, phone, and ID column types, with user override. |
| FR-05 | Sort by one or more columns, including ascending, descending, and user-defined orders. Text must sort alphabetically, numbers numerically, and dates chronologically. |
| FR-06 | Clean selected headers and values: trim whitespace, remove fully blank rows/columns, standardize headers, dates, phone numbers, emails, roll numbers, and names. |
| FR-07 | Flag invalid or missing values without silently removing them. |
| FR-08 | Detect, preview, and remove exact duplicates; detect near duplicates using user-selected comparison columns and a reviewable match rule. Users choose whether to keep first, keep last, or review. |
| FR-09 | Filter using text contains, exact match, numeric range, or date range; combine filters with AND or OR. |
| FR-10 | Split processed data into separate Excel sheets using one selected column. |
| FR-11 | Save, load, update, delete, and apply named Recipes containing cleaning, sort, filter, deduplication, and split settings. |
| FR-12 | Export a new formatted `.xlsx` file with a Summary sheet. The export includes bold headers, a frozen header row, filters, and sensible column widths. |
| FR-13 | Generate a processing summary: original/final rows, blank rows removed, duplicates removed, invalid values flagged, columns modified, and processing time. |
| FR-14 | Record audit events for processing and export, including actor (where identity is available), file name, recipe, timestamp, row count, and outcome; allow administrators to view them. |

### Non-functional requirements

| Area | Requirement |
|---|---|
| Performance | Process a representative 50,000-row workbook in under 30 seconds on agreed normal college hardware, excluding a user’s upload/download network time. |
| Data integrity | Never overwrite or mutate the uploaded source. All transformations create an in-memory or new export result. |
| Resilience | Safely handle missing values, merged headers, blank rows, inconsistent types, and duplicate/blank column names. |
| Usability | Use plain-language messages, clear previews, and visible counts before destructive-looking actions. |
| Privacy | Minimize retained student data; do not transmit files to third parties by default. |
| Deployment | Support local Windows use and self-hosted college-server deployment. |
| Reliability | Failed validation or export must leave no partially modified source file and provide a recoverable next action. |

### Success metrics

- Reduce report-preparation time by at least 50% compared with the department's current manual process.
- Reduce duplicate-record errors in standard reports to near zero, measured against an agreed manual audit sample.
- Generate a standard report in under two minutes from upload to download for the pilot workflow.
- Achieve at least 80% unassisted task completion in pilot usability tests.

## 2. Personas

### Exam Cell Coordinator

Prepares examination lists from files supplied by departments. Needs to sort reliably by roll number, subject, and department, remove accidental repeat records, and reuse a known exam-report setup every cycle. Their biggest concern is publishing an incorrect or incomplete list.

### Placement Officer

Receives placement data from students, faculty, and companies with inconsistent branch, company, and status labels. Needs to clean it, filter cohorts, and produce branch- or company-specific sheets quickly.

### Attendance Officer

Combines attendance extracts to identify students below a threshold (commonly 75%). Needs date and percentage values handled consistently and department-wise reports generated without manually copying rows.

### College Administrator

Needs standard departmental outputs, confidence that sensitive student data has not been retained unnecessarily, and a trustworthy activity history. This persona administers recipes and reviews audit logs; account/role controls are a deployment decision, not assumed in the first MVP.

## 3. User stories and acceptance criteria

| ID | User story | Acceptance criteria |
|---|---|---|
| US-01 | As an Exam Cell Coordinator, I want to upload an exam file so I can prepare a report. | Given a valid Excel or CSV file, when uploaded, SheetSort shows filename, row/column counts, timestamp, and the first 10 parsed rows. |
| US-02 | As a staff member, I want usable headers from an imperfect file. | Given blank or duplicate headers, when the schema is detected, SheetSort shows unique safe display names and flags the issue for review rather than losing a column. |
| US-03 | As an Exam Cell Coordinator, I want to sort by department, subject, and roll number. | Given three selected sort rules, when applied, records follow priority order and their detected types; no selected sort leaves source row order unchanged. |
| US-04 | As a Placement Officer, I want to clean inconsistent contact and branch data. | Given enabled cleaning rules, when processing completes, selected transformations are applied and invalid emails/phones remain present but are flagged in the summary. |
| US-05 | As an Attendance Officer, I want a low-attendance report. | Given an attendance column and a numeric filter below 75, when filtering is applied, only matching records remain in the preview and export. |
| US-06 | As a staff member, I want to review duplicates before removal. | Given exact or configured near duplicates, when duplicate detection runs, SheetSort displays the affected rows and allows keep-first, keep-last, or no removal. |
| US-07 | As a Placement Officer, I want department sheets from one file. | Given a selected split column, when exported, the workbook includes a distinct safely named sheet for each selected value plus a Summary sheet. |
| US-08 | As a repeat user, I want to reuse a Recipe. | Given a saved Recipe, when I apply it to a compatible new file, its stored rules are loaded and any missing referenced columns are clearly identified before export. |
| US-09 | As a College Administrator, I want accountability for processing. | Given completed processing or export, when I open the audit log, I can view the action, available actor, filename, recipe, timestamp, rows processed, and outcome. |
| US-10 | As a staff member, I want an export I can send immediately. | Given a successful processing run, when I export, I receive a new `.xlsx` workbook with formatted data and a Summary sheet containing all required counts and processing time. |

## 4. MVP feature list

The MVP includes upload/validation, schema detection and override, preview, sorting, selected cleaning operations, filtering, exact and reviewable near-duplicate handling, splitting, formatted Excel export, Recipes in local storage, processing summaries, and administrator-visible audit logs.

The MVP deliberately excludes user lifecycle management, SSO, ERP integration, cloud multi-tenancy, PDF export, bulk queues, and collaborative editing. These belong to the post-pilot roadmap unless a pilot requirement changes scope.

## 5. Future roadmap

| Horizon | Candidate capability | Outcome |
|---|---|---|
| Post-pilot | User accounts, roles, and college SSO | Role-aware recipe and audit access. |
| Post-pilot | Bulk file processing and template validation | Repeatable high-volume departmental workflows. |
| Expansion | Pivot-style summaries and PDF export | Broader reporting without manual spreadsheet work. |
| Expansion | Google Sheets and ERP/SIS integration | Reduced import/export handoffs. |
| Expansion | Multi-language UI and managed cloud deployment | Wider adoption and deployment flexibility. |

## 6. Technical and delivery risks

| Risk | Impact | Mitigation / decision needed |
|---|---|---|
| Large or complex workbooks exceed the performance target | Slow or failed processing | Benchmark representative 50,000-row files; set size limits and optimize only measured bottlenecks. |
| Legacy `.xls`, formulas, macros, or merged-cell layouts parse inconsistently | Data loss or confusing previews | Read values only, reject unsupported/macro behavior clearly, and test real departmental samples. |
| Near-duplicate matching produces false matches | Records may be removed incorrectly | Require selected key columns and preview; default to no deletion until user confirms. |
| Ambiguous dates (for example `03/04/2026`) | Incorrect standardization | Use a configurable locale/date policy and flag unparseable or ambiguous values. |
| Sensitive student data persists in logs, browser state, exports, or backups | Privacy/compliance exposure | Retain metadata only by default; define retention, access, encryption, and backup policies before pilot. |
| SQLite is unsuitable for concurrent multi-user server workloads | Recipe/audit contention or availability issues | Suitable for local/small pilot; define concurrency threshold and migration path before college-wide rollout. |
| No confirmed authentication model | Audit actor identity cannot be trusted | Decide whether MVP is single-user/local, shared authenticated server, or integrated with existing identity. |
| Data-cleaning expectations vary by department | Recipes may not be safely portable | Make rules explicit, preview results, and pilot with sample files from each participating department. |

## 7. Stage-gate assumptions

1. The first release is a self-hosted tool for one college and does not use external AI or cloud file processing.
2. Uploaded files are processed transiently; only Recipes and audit metadata persist by default.
3. The initial audit actor may be a supplied display name or local operator identity until authentication is formally chosen.
4. `DD-MM-YYYY` is the export date display format; parsing policy for ambiguous source dates must be confirmed before production use.
5. “Normal hardware” will be defined during Stage 1 performance planning (CPU, RAM, storage, and representative workbook shape).
6. The MVP must preserve row data unless a user explicitly selects a removal action; flags and summaries are preferred to silent correction.

## 8. Stage 0 handover

### Completed

- Defined the product scope, value proposition, goals, non-goals, functional and non-functional requirements, success metrics, and personas.
- Added testable user stories with acceptance criteria.
- Defined the MVP boundary, post-MVP roadmap, assumptions, and delivery risks.

### Decisions still needed before implementation design

1. Is the first pilot a single local operator, a shared college-server instance, or a shared instance with login?
2. Which jurisdiction/institutional retention and privacy policy governs uploaded-file, export, and audit-log retention?
3. Should ambiguous numeric dates default to day-first (common for the requested `DD-MM-YYYY` output), or require explicit user selection?
4. What hardware and representative files define the 50,000-row performance target?

### Next-stage checklist

- [ ] Confirm or revise the four outstanding decisions above.
- [ ] Approve this Stage 0 baseline.
- [ ] Proceed to Stage 1: architecture, data models, pipeline, service contracts, and security design.
