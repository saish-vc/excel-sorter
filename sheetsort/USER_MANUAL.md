# SheetSort - User Manual

*For college administrative staff - Exam Cell, Admissions Office, Placement Cell, Attendance Office*

## 📋 Quick Start (1-Page)

### Step 1: Upload Your File
1. Open SheetSort in your web browser
2. Click "Browse" or drag & drop your Excel/CSV file
3. Accepted formats: `.xlsx`, `.xls`, `.csv`
4. Maximum size: 50 MB or 100,000 rows
5. Click "Upload"

### Step 2: Review the Preview
- The app shows your first 10 rows
- Verify the data looks correct
- Note the row and column count

### Step 3: Detect Headers & Column Types
1. Click "Schema Detection" tab
2. The app automatically detects the header row
3. Column types are detected (text, number, date, email, phone, ID)
4. You can override any detected type if needed
5. Click "Continue" or "Use Detected Schema"

### Step 4: Clean the Data
1. Go to "Cleaning" tab
2. Select which operations to apply:
   - ✓ Trim spaces (removes leading/trailing spaces)
   - ✓ Remove empty rows
   - ✓ Remove empty columns
   - ✓ Standardize headers (lowercase, underscores)
   - ✓ Convert dates to DD-MM-YYYY format
   - ✓ Normalize phone numbers
   - ✓ Validate and flag invalid emails
   - ✓ Flag invalid/missing values
3. Click "Apply Cleaning"

### Step 5: Sort the Data
1. Go to "Sorting" tab
2. Add sort rules:
   - Select column to sort by
   - Choose ascending or descending
   - Optional: use custom order (e.g., Department: CSE, IT, ECE, Mechanical)
   - Set priority for multi-column sorting
3. Click "Apply Sorting"

### Step 6: Filter the Data
1. Go to "Filtering" tab
2. Add filter rules:
   - Text: contains or exact match
   - Numeric: greater than, less than, between
   - Date: date range
   - Combine with AND/OR logic
3. Click "Apply Filters"

### Step 7: Remove Duplicates
1. Go to "Deduplication" tab
2. Select options:
   - Keep: first or last duplicate
   - Subset columns (optional - only check these columns)
   - Detect near-duplicates (optional - similarity threshold)
3. Click "Remove Duplicates"

### Step 8: Split Data (Optional)
1. Go to "Splitting" tab
2. Select column to split by (e.g., Department, Year, Batch)
3. Enter sheet name prefix (e.g., "Dept_")
4. Check "Include header in each sheet" (usually yes)
5. Click "Split Data"

### Step 9: Save as Recipe (Optional)
1. Go to "Export & Recipes" tab
2. Enter recipe name and description
3. Click "Save Current Workflow as Recipe"
4. Your cleaning, sorting, filtering, and split settings are saved
5. You can load this recipe later for similar files

### Step 10: Export the Report
1. Go to "Export & Recipes" tab
2. Review the processed data preview
3. Click "Generate Summary and Export"
4. Download the `.xlsx` file containing:
   - **Data sheet**: Your cleaned, sorted, filtered data with formatting
   - **Summary sheet**: Statistics about the processing

### 🎯 Common Tasks for Each Persona

#### Exam Cell Coordinator
- Upload exam roster → Sort by roll number → Remove duplicates → Export rank list
- Save as "Exam Report" recipe for future exam periods

#### Placement Officer
- Upload placement data → Filter by "Placed" status → Split by branch → Export per-branch reports
- Save as "Placement Workflow" recipe

#### Attendance Officer
- Upload attendance file → Filter students <75% attendance → Split by department → Export summary
- Save as "Attendance Report" recipe

#### College Administrator
- Review audit log of all file-processing actions
- Manage user access and recipes
- Backup and restore the system

---

## ⚙️ Understanding the Interface

### Tabs/ Pages
1. **Upload & Preview** - File upload and initial data view
2. **Schema Detection** - Header and column type detection
3. **Cleaning** - Data cleaning operations
4. **Sorting** - Multi-column sorting
5. **Filtering** - Data filtering
6. **Deduplication** - Duplicate removal
7. **Splitting** - Split into separate sheets
8. **Export & Recipes** - Export and recipe management
9. **Audit Log** - View processing history

### Data Types Recognized
- **Text**: General strings, names, addresses
- **Number**: Numeric values, marks, IDs
- **Date**: Dates in various formats (converted to DD-MM-YYYY)
- **Email**: Email addresses (validated format)
- **Phone**: Phone numbers (normalized format)
- **ID**: Identification numbers

### Error Messages You Might See
- "The file is empty. Please upload a file with data."
- "Unsupported file type. Please upload .xlsx, .xls, or .csv."
- "The file too large. Maximum size is 50 MB."
- "Could not detect a header row. Please confirm which row contains column names."
- "Some dates could not be parsed (DD-MM-YYYY). They have been flagged for review."
- "The uploaded file could not be processed. Please check the format and try again."

---

## 🆘 Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| "File too large" | Compress the file or split into multiple files (max 100K rows) |
| "Unsupported file type" | Ensure file is .xlsx, .xls, or .csv (not .xlsxm or other macros-enabled types) |
| "Could not detect a header row" | Go to Schema Detection tab and manually specify the header row number |
| "Some dates could not be parsed" | Go to Cleaning tab and enable "Convert dates to DD-MM-YYYY", or check date format in your file |
| "Invalid email format flagged" | This is informational - emails are flagged but not removed. Review and correct as needed. |
| "Application slow with 50K rows" | This is normal for first processing. Subsequent runs are faster due to caching. |
| "Duplicate rows found" | Go to Deduplication tab and choose to keep first or last occurrence |

---

## 📊 Understanding Your Export

The exported `.xlsx` file contains two sheets:

### 1. Data Sheet
- Your cleaned, sorted, and filtered data
- Formatting includes:
  - Bold header row
  - Frozen header row (stays visible when scrolling)
  - Auto-adjusted column widths
  - Filter buttons enabled (drop-down arrows in header)

### 2. Summary Sheet
Contains processing statistics:
- **Original Row Count**: Rows before processing
- **Final Row Count**: Rows after all operations
- **Duplicates Removed**: How many duplicate rows were eliminated
- **Blank Rows Removed**: How many empty rows were cleaned
- **Invalid Values Flagged**: How many cells had invalid data (flagged, not removed)
- **Columns Modified**: How many columns had changes applied
- **Processed On**: Date and time when processing was completed

---

## 🔒 Security & Privacy Notes

- **Original files are never modified**: A temporary copy is used for processing
- **Data is processed in memory**: Only the final Excel file is written to disk
- **No external data transmission**: All processing happens locally (unless using cloud deployment)
- **Audit log tracks actions**: Records what was done, when, and how many rows - but does not store sensitive PII
- **Use anonymized data for evaluation**: Consider removing roll numbers, names, etc. when evaluating the tool

---

## 💡 Tips & Best Practices

1. **Start with sample data**: Use the provided sample files to learn the workflow
2. **Save recipes**: Once you find a working setup (cleaning + sorting + filters), save it as a recipe for future use
3. **Check the preview always**: Review each step's output before proceeding to the next
4. **Use subset columns for duplicates**: If your data has many columns but duplicates are based on few key columns, use the "subset columns" option
5. **AND vs OR filters**: 
   - AND: All conditions must be met (narrows results)
   - OR: Any condition can be met (broadens results)
6. **Custom sort orders**: For department columns, always use custom order (CSE, IT, ECE, Mechanical, etc.) for correct ordering
7. **Backup recipes**: Export your .env file or note your recipe names for future deployments

---

## 📞 Need Help?

- **Check the Audit Log**: See what processing actions have been performed
- **Review this manual**: Most common questions are answered here
- **Contact support**: If issues persist, note the error message and when it occurred
- **Backup regularly**: Especially the recipes.db SQLite file

---
*SheetSort - Turn messy Excel files into clean, sorted reports in minutes.*
*Designed for college administrative departments.*