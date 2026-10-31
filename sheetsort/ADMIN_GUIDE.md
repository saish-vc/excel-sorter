# SheetSort - Admin Guide

*For college IT administrators and system managers*

## 👥 User Management

### Adding New Users

SheetSort is designed for single-user or limited multi-user deployments. User management depends on the deployment type:

#### Single-User (Local/College Server)
- Each staff member runs SheetSort independently
- Recipes and audit logs are individual
- No central user database needed

#### Limited Multi-User (Same Server)
1. **Shared Recipes Database**
   - All users share the same `recipes.db` SQLite database
   - Recipes saved by one user are available to all
   - Location: Set via `SHEETSORT_RECIPE_DB` environment variable

2. **Access Control**
   - File system permissions control who can access the Streamlit app
   - Place the app behind a college authentication system (SSO, Active Directory)
   - Each user has their own Windows/macOS login

### Recipe Sharing

#### How Recipes Are Shared
1. Recipes are stored in the central `recipes.db` SQLite database
2. Any user with access to the app can:
   - View existing recipes (List Recipes page)
   - Load and apply existing recipes
   - Save new recipes from their own workflow
   - Update or delete recipes they created

3. **Recipe Ownership**
   - Each recipe has an `is_active` flag
   - The system admin can manage recipe visibility
   - Recipes can be marked as "active" or "archived"

#### Best Practices for Recipe Management
- Create department-specific recipes (Exam Report, Placement Workflow, Attendance Report)
- Mark frequently-used recipes as `is_active: true`
- Archive obsolete recipes rather than deleting them
- Review and clean up recipes quarterly

---

## 📊 Recipe Management

### Viewing Recipes

1. Navigate to "Export & Recipes" tab
2. Click "Your Recipes" section
3. List shows:
   - Recipe name
   - Date created
   - Whether it's marked as active

### Saving a New Recipe

1. Complete your data processing workflow (upload → clean → sort → filter → split → export)
2. Go to "Export & Recipes" tab
3. Enter recipe name (e.g., "Exam Report")
4. Optional: Enter description (e.g., "For end-of-semester exam rank lists")
5. Click "Save Current Workflow as Recipe"
6. The recipe is saved to the SQLite database

### Updating a Recipe

1. Go to "Your Recipes" section
2. Find the recipe to update
3. Click the recipe name or use update functionality
4. Modify:
   - Name
   - Description
   - Sort rules
   - Filter rules
   - Cleaning rules
   - Split rule
5. Click "Save Changes"

### Deleting a Recipe

1. Go to "Your Recipes" section
2. Find the recipe to delete
3. Click delete/remove
4. Confirm deletion
5. The recipe is permanently removed from the database

### Recipe Format (SQLite Structure)

Recipes are stored in a `recipes` table with columns:
- `recipe_id` (TEXT, PRIMARY KEY, UUID)
- `name` (TEXT)
- `created_ts` (TEXT, ISO timestamp)
- `sort_rules` (TEXT, JSON)
- `filter_rules` (TEXT, JSON)
- `cleaning_rules` (TEXT, JSON)
- `split_rule` (TEXT, JSON or "None")
- `description` (TEXT)
- `is_active` (INTEGER, 0 or 1)

---

## 📋 Audit Log Review

### What's Logged

The audit log records all processing actions in the `audit_log` SQLite table:

| Field | Description |
|-------|-------------|
| `entry_id` | Unique identifier for this log entry |
| `user_action` | Type of action (upload, process, recipe_save, recipe_load, recipe_delete, export) |
| `file_id` | UUID of the uploaded file (if applicable) |
| `recipe_id` | UUID of the recipe used (if applicable) |
| `timestamp` | When the action occurred |
| `rows_processed` | How many rows were in the input |
| `rows_exported` | How many rows made it to the output |
| `notes` | Free-form notes (e.g., error type, additional info) |

### Accessing the Audit Log

1. **Via the Application**
   - Go to "Audit Log" tab/page
   - View recent entries (last 20 by default)
   - Filter/sort as needed

2. **Via SQLite Database**
   ```bash
   # Query the audit log
   sqlite3 recipes.db "SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT 10;"
   
   # Example queries
   # See all export actions
   sqlite3 recipes.db "SELECT * FROM audit_log WHERE user_action='export';"
   
   # See processing by date range
   sqlite3 recipes.db "SELECT * FROM audit_log WHERE timestamp > '2024-01-01';"
   ```

### Sample Audit Log Entries

| entry_id | user_action | file_id | recipe_id | timestamp | rows_processed | rows_exported | notes |
|----------|-------------|---------|-----------|-----------|----------------|---------------|-------|
| `abc123` | export | `def456` | `exam_report` | 2024-01-15 14:30:00 | 50 | 45 | Successful export |
| `def456` | upload | `ghi789` | NULL | 2024-01-15 10:15:00 | 0 | 0 | New file upload |
| `ghi789` | process | `def456` | `exam_report` | 2024-01-15 10:20:00 | 50 | 45 | Exam report processed |

### Audit Log Best Practices

1. **Review weekly**: Check the audit log at least once per week
2. **Monitor for anomalies**: Look for unusual row counts or actions
3. **Track recipe usage**: See which recipes are most frequently used
4. **Identify training needs**: If many errors occur, consider additional staff training
5. **Retention policy**: Keep audit logs for 90 days minimum, 1 year recommended

### Exporting the Audit Log

1. **Via SQLite command**
   ```bash
   sqlite3 recipes.db ".mode csv" ".separator," ".output audit_log.csv" "SELECT * FROM audit_log;"
   sqlite3 recipes.db ".mode list" ".separator|" ".output audit_log.txt" "SELECT * FROM audit_log;"
   ```

2. **Via the application**
   - Use the "Export" functionality which includes audit information
   - Manual copy from the Audit Log page

---

## 💾 System Backup

### What to Backup

1. **Recipes Database** (`recipes.db` or custom path from `.env`)
   - Contains all saved workflows
   - Critical for business continuity
   - Small file size (~few MB even with many recipes)

2. **Sample Data Files** (`sample_data/` directory)
   - Used for demos and testing
   - Can be regenerated if needed
   - Backup for consistency

3. **Logs** (if enabled, `logs/` directory)
   - Application log files
   - Help with troubleshooting
   - Can grow large over time

4. **Configuration** (`.env` file)
   - Environment variables
   - Custom settings
   - Small file size

### Backup Procedure

#### Manual Backup

```bash
# 1. Stop the Streamlit app if running

# 2. Backup the recipes database
copy recipes.db backup_recipes_%DATE%.db

# 3. Backup sample data
xcopy sample_data\*.* backup_samples_%DATE%.\*

# 4. Backup logs (if applicable)
xcopy logs\*.* backup_logs_%DATE%.\*

# 5. Backup configuration
copy .env backup_env_%DATE%.env

# 6. Start the app again
streamlit run app\main.py
```

#### Automated Backup (Recommended)

Set up Windows Task Scheduler:

1. **Open Task Scheduler** (taskschd.msc)
2. **Create Basic Task** → Name: "SheetSort Daily Backup"
3. **Trigger**: Daily at 23:00
4. **Action**: 
   - Program/script: `cmd.exe`
   - Add arguments: `/c cd /d %USERPROFILE%\sheetsort && backup.bat`
5. **Finish**

Create `backup.bat` in the sheetsort folder:
```batch
@echo off
set DATE=%DATE:~10,4%%DATE:~4,2%%DATE:~7,2%
copy recipes.db backup_recipes_%DATE%.db
xcopy sample_data\*.* backup_samples_%DATE%.\* /Y
xcopy logs\*.* backup_logs_%DATE%.\* /Y
copy .env backup_env_%DATE%.env
echo Backup completed at %TIME%
```

### Restore Procedure

1. **Stop the Streamlit app**
2. **Copy backup files back**:
   ```bash
   copy backup_recipes_20240101.db recipes.db
   xcopy backup_samples_20240101.* sample_data\ /Y
   xcopy backup_logs_20240101.* logs\ /Y
   copy backup_env_20240101.env .env
   ```
3. **Start the Streamlit app**
   ```bash
   streamlit run app\main.py
   ```
4. **Verify**: Log in and check that recipes are restored

### Backup Retention Policy

| Duration | What to Keep |
|----------|--------------|
| **Daily** | Last 7 days of backups |
| **Weekly** | Last 4 weeks (1 month) |
| **Monthly** | Keep 3 months of monthly backups |
| **Quarterly** | Archive to long-term storage |

---

## 🔧 Troubleshooting Guide

### Common Issues

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| App won't start | Python not in PATH | Add Python to System PATH |
| "Port 8501 already in use" | Another app using the port | Change port: `streamlit run --server.port 8502 app\main.py` |
| File upload fails | Unsupported file format | Use .xlsx, .xls, or .csv only |
| "File too large" | Over 100K rows or 50 MB | Split file or increase limit in .env |
| Cleaning not applying | Checkboxes not selected | Ensure cleaning operation checkboxes are ticked |
| Sort not working | Custom order not set | Use custom order for department/column sorting |
| Filters returning no results | Too restrictive | Try OR logic or remove some filter conditions |
| Duplicates not detected | Subset columns not selected | Select only the key columns to check for duplicates |
| Export fails | Openpyxl format issue | Re-save Excel file, check for corruption |
| Recipes not loading | Database corruption | Delete recipes.db, restart app, re-save recipes |
| Slow performance with 50K rows | Normal for first run | Subsequent runs faster; consider Docker for production |

### Error Logs

1. **Application Logs**
   - Location: `logs/` directory (if enabled)
   - Level: Set via `SHEETSORT_LOG_LEVEL` env var
   - Format: `YYYY-MM-DD HH:MM:SS | LEVEL | Logger | Message`

2. **Common Error Messages**
   - `ModuleNotFoundError: No module named 'openpyxl'` → `pip install openpyxl`
   - `PermissionError: [Errno 13] Permission denied` → Run as Administrator
   - `sqlite3.OperationalError: database is locked` → Close other connections to the DB
   - `ValueError: could not convert string to datetime` → Check date format in data

### When to Contact Support

- Error messages not covered in this guide
- Data loss or corruption suspected
- Performance issues beyond expected norms
- Integration questions with college systems
- Feature requests or enhancement ideas

---

## 📊 Performance Guidelines

### Expected Processing Times

| Data Size | Expected Time |
|-----------|--------------|
| 1,000 rows | < 5 seconds |
| 5,000 rows | ~10 seconds |
| 10,000 rows | ~15 seconds |
| 25,000 rows | ~20 seconds |
| 50,000 rows | ~30 seconds |
| 100,000 rows | ~45 seconds |

### Optimization Tips

1. **Use recipes**: Once a workflow is saved, applying it to new files is much faster
2. **Skip unnecessary steps**: Disable cleaning operations you don't need
3. **Limit column subsets**: For duplicate detection, only check key columns
4. **Use appropriate filter specificity**: Too many filters can slow processing
5. **For production use**: Deploy via Docker with proper resources

### Resource Requirements

| Deployment Type | RAM | CPU | Storage |
|----------------|-----|-----|---------|
| Local (small files < 5K rows) | 2GB | 2 cores | 500MB |
| College Server (medium files < 25K rows) | 4GB | 4 cores | 1GB |
| Docker/Production (50K rows) | 8GB | 4+ cores | 2GB |

---

## 📞 Contact & Support

### For This Pilot

- **Pilot Coordinator**: [Name/Department]
- **Duration**: 60-90 days
- **Check-ins**: Weekly (template in pilot package)
- **Feedback form**: Included in pilot package

### General Support

- **Review this Admin Guide** first
- **Check the Audit Log** for processing history
- **Backup the recipes.db** before making major changes
- **Contact**: [IT Department contact information]

### Feature Requests

- Submit feature requests to the development team
- Priority given to requests that improve usability for college staff
- Considered for future roadmap updates

---
*SheetSort Admin Guide - For college IT administrators and system managers*
*Managing user access, recipes, audits, and backups*