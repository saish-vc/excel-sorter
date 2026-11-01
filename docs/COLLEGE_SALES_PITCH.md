# 🎓 SheetSort: College Commercial Sales Pitch & Demonstration Pack

This kit provides everything needed to pitch, demonstrate, and sell **SheetSort** to engineering colleges, polytechnics, arts & science colleges, and university administrative bodies.

---

## 1. Executive Proposal Letter (For Principals, Deans & HODs)

```text
To,
The Principal / Dean of Academics / Head of Department,
[College Name]
[City, State]

Subject: Proposal for Automating College Data Processing & Spreadsheet Workflows with SheetSort

Respected Sir / Madam,

Every academic semester, our administrative staff, Examination Cell, and Training & Placement Cell 
spend hundreds of manual hours wrangling student spreadsheets—cleaning inconsistent roll number formats, 
fixing broken date entries, removing duplicate applicant records, and manually splitting master rosters 
into department-wise sheets.

This manual process not only leads to administrative exhaustion and delays in report submissions, 
but also introduces human transcription errors and risks student data confidentiality when online conversion 
utilities are used.

To solve this, we have developed SheetSort—an intelligent, air-gapped desktop platform designed specifically 
for academic institutions:

Key Capabilities for [College Name]:
1. 1-Click Roster Standardization: Automatically trims whitespaces, normalizes 10-digit phone numbers, 
   standardizes dates to DD-MM-YYYY, and flags invalid student emails.
2. Departmental Splitting in Seconds: Automatically splits a university-wide master marks or registration file 
   into separate department worksheets (CSE, IT, ECE, Mechanical, etc.) in a single styled Excel workbook.
3. Automated Defaulter & Placement Filtering: Instantly filter students below 75% attendance or filter eligible 
   placement candidates meeting multi-criteria cut-offs without writing a single Excel macro.
4. 100% Student Data Privacy: Operates completely offline on standard college desktop PCs without uploading 
   any student data to cloud servers.
5. Reusable "Recipe" Engine: Record a routine workflow once and replay it on fresh student files in 1 click.

We would be pleased to provide a 20-minute on-campus demonstration using real or sample college datasets, 
along with a complimentary 60-day pilot for one department (e.g., Examination or Placement Cell).

Thank you for your time and consideration.

Sincerely,
Saish Sawant (Developer & Maintainer)
sunilsawant6812@gmail.com | https://github.com/saish-vc/excel-sorter
```

---

## 2. 5-Minute Live Demo Script (Step-by-Step)

When pitching to college authorities, follow this scripted demonstration using the included sample datasets in `sample_data/`:

### Step 1: Launch & Local Isolation (30 Seconds)
- Double-click `SheetSort.exe` (or run `desktop_launcher.py`).
- **Pitch Point:** *"Notice that this runs immediately in your local browser on loopback (127.0.0.1). No command line, no Python knowledge needed for staff, and zero student data leaves this PC."*

### Step 2: Upload Messy Exam File (1 Minute)
- Navigate to **Upload & Preview**.
- Upload `sheetsort/sample_data/exam_roster.xlsx`.
- Point out the instant data preview, total rows (50 records), and validated file metadata.

### Step 3: Header Detection & Cleaning (1.5 Minutes)
- Go to **Schema Detection** & click **Detect Header Row**. Explain how it ignores messy top title banners.
- Move to **Cleaning**. Check:
  - *Trim leading/trailing spaces*
  - *Standardize headers*
  - *Convert dates to DD-MM-YYYY*
- Click **Apply Cleaning Operations**. Point out the summary metrics showing exactly how many rows were standardized.

### Step 4: Sorting & Department Splitting (1.5 Minutes)
- Go to **Sorting**: Add Sort Rule -> Column `Department`, Order `ascending`, or set custom academic order (`CSE, IT, ECE, Mechanical`).
- Go to **Splitting**: Select `Split by column` -> `Department`, sheet prefix `Dept_`.
- Click **Split Data**. Show how it generated separate sheets for each branch with individual row counts.

### Step 5: Save Recipe & Export (30 Seconds)
- Go to **Export & Recipes**: Name the recipe *"Semester Exam Standardizer"* and click **Save Current Workflow as Recipe**.
- Click **Generate Summary and Export** -> Download the resulting `.xlsx` file.
- Open the exported Excel file in Microsoft Excel to show:
  - Bold, frozen headers.
  - Active auto-filters.
  - Dedicated tabs per department.
  - An executive **Summary tab** ready for the Principal's signature.

---

## 3. Objection Handling Guide

| Typical College Objection | Proven Counter-Response |
|---|---|
| *"Doesn't Microsoft Excel already do sorting and filtering?"* | Excel requires staff to manually repeat 15–20 clicks, formulas, and VLOOKUPs every single time a file arrives. SheetSort packages the entire process into a **1-click reusable Recipe**. Anyone on staff can run it with zero errors. |
| *"Is student data secure from leaks?"* | Yes. SheetSort is **completely air-gapped**. It contains no internet telemetry, runs strictly in RAM, and never transmits data outside the physical PC. |
| *"Do we need to upgrade our lab or office computers?"* | No. SheetSort runs on any standard Windows 10/11 computer with an Intel Core i3 processor and 4 GB RAM. |
| *"Will it work with our university ERP/portal exports?"* | Yes. It natively ingests exports from any college portal (SAP, ERP, Google Forms, NAAC portals) in `.xlsx`, `.xls`, or `.csv` format. |
| *"What if our staff makes a mistake during cleaning?"* | The original file is never overwritten. Every processing run is logged in the built-in tamper-evident **Audit Log**. |

---

## 4. Commercial Pricing Structure

### Package A: Single Department License
- **Target:** Examination Cell OR Training & Placement Cell.
- **Includes:** Installation on up to 3 PCs, 5 custom pre-built college recipes, 1-hour staff training, 1 year of software updates.
- **Price:** **₹10,000 – ₹15,000** (One-time perpetual) or **₹5,000/year**.

### Package B: Campus-Wide Institutional License (Recommended)
- **Target:** Whole College (Exam Cell, T&P Cell, Admissions, All Academic Departments, Principal Office).
- **Includes:** Unlimited PC installations across the campus network, unlimited custom recipes, full staff training workshop, priority support, and audit log compliance reporting.
- **Price:** **₹25,000 – ₹40,000** (One-time perpetual) + optional ₹5,000/year annual maintenance & updates.
