# SheetSort - College Data Processing App

A web application for college administrative staff to clean, sort, standardize, and export Excel/CSV files.

## Quick Start

### Local Installation

1. **Clone or download** the project
2. **Install dependencies**:
   ```bash
   pip install -r sheetsort/requirements.txt
   ```
3. **Run the app**:
   ```bash
   streamlit run sheetsort/app/main.py
   ```
4. **Open your browser** to `http://localhost:8501`

### Docker Deployment

```bash
# Build the image
docker build -t sheetsort .

# Run the container
docker run -p 8501:8501 sheetsort
```

Access at `http://localhost:8501`

### Docker Compose (for production)

```yaml
version: '3.8'
services:
  sheetsort:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/home/appuser/data
    environment:
      - SHEETSORT_LOG_LEVEL=INFO
```

## How It Works

1. **Upload** - Accepts .xlsx, .xls, and .csv files (max 50 MB or 100K rows)
2. **Schema Detection** - Auto-detects header row and column data types
3. **Cleaning** - Trims spaces, removes empties, standardizes headers, converts dates, normalizes phones, validates emails
4. **Sorting** - Multi-column sort with ascending/descending and custom order
5. **Filtering** - Text, numeric, and date range filters with AND/OR logic
6. **Deduplication** - Exact and near-duplicate removal
7. **Splitting** - Split data into separate sheets by selected column
8. **Export** - Export to .xlsx with a Summary sheet and preserved formatting

## Features

- **File Upload**: .xlsx, .xls, .csv with validation
- **Schema Detection**: Automatic header detection and column type inference
- **Cleaning Operations**: 8 cleaning rules configurable by the user
- **Sorting**: Multi-column with custom order support (e.g., Department: CSE, IT, ECE)
- **Filtering**: Text contains, exact match, numeric ranges, date ranges
- **Deduplication**: Exact duplicates + near-duplicate detection
- **Splitting**: Split by any column (Department, Year, Batch, etc.)
- **Recipes**: Save/reuse complete workflows
- **Audit Log**: Track all processing actions
- **Export**: Formatted .xlsx with Summary sheet

## Project Structure

```
sheetsort/
├── app/
│   ├── main.py                # Streamlit entry point
│   ├── ui/
│   │   └── pages/             # Streamlit page modules
│   ├── services/              # Business logic services
│   │   ├── upload_service.py
│   │   ├── schema_detection.py
│   │   ├── data_cleaning.py
│   │   ├── sorting.py
│   │   ├── filtering.py
│   │   ├── deduplication.py
│   │   ├── splitting.py
│   │   ├── recipe_service.py
│   │   └── export_service.py
│   ├── models/                # Data models (typed dicts)
│   │   ├── uploaded_file.py
│   │   ├── column_metadata.py
│   │   ├── sort_rule.py
│   │   ├── filter_rule.py
│   │   ├── cleaning_rule.py
│   │   ├── split_rule.py
│   │   ├── recipe.py
│   │   ├── processing_result.py
│   │   └── audit_log_entry.py
│   ├── utils/
│   │   ├── config.py          # Constants and configuration
│   │   ├── logger.py
│   │   └── exceptions.py
│   └── __init__.py
├── sample_data/               # Anonymized college data samples
├── tests/                     # pytest test files
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

## Sample Data

The `sample_data/` directory contains anonymized Excel/CSV files for testing and demonstrations:

- `exam_roster.xlsx` - Student exam records with roll numbers, subjects, departments
- `placement_data.csv` - Placement data with company names, branches
- `attendance_sample.csv` - Attendance records with dates and percentages

To generate your own sample data, use the sample data generator or create files matching the expected formats.

## Security & Privacy

- Original uploaded files are never modified; a temporary copy is used
- All processing occurs in memory; only the final .xlsx is written to disk
- SQLite database stores recipes and audit metadata (not raw file data)
- No external APIs or data transmission (local deployment only)
- Audit logs record actions without storing sensitive PII

## Configuration

Copy `.env.example` to `.env` and adjust as needed:

```
# See sheetsort/app/utils/config.py for defaults
SHEETSORT_LOG_LEVEL=INFO
SHEETSORT_RECIPE_DB=recipes.db
```

## License

This project is licensed under the MIT License.