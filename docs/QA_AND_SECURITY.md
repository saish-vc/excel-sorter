# QA and Security Validation

## Automated coverage

The pytest suite verifies file validation, parsing, schema detection, cleaning, sorting, filters, exact and near duplicate handling, splitting, Excel export, and Recipe persistence. Regression tests cover keep-last deduplication and formula-like values in exported cells.

## Security checks

- Only .xlsx, .xls, and .csv filenames are accepted and byte/row limits are enforced.
- SQLite uses parameterized values for stored recipe/audit data.
- Exported strings starting with =, +, -, or @ are written as text.
- Raw uploaded content is not deliberately persisted.
- No secrets, shell execution, dynamic code execution, or external data services are used by the application.

## Manual UAT checklist

- Exam Cell: upload a roster, sort by department/subject/roll number, export.
- Placement: normalize data, remove reviewed duplicates, split by branch, export.
- Attendance: filter below 75%, split by department, export.
- Administrator: save/load/delete a Recipe and review audit events.

## Performance method

Run the same workflow for 1,000, 10,000, 50,000, and 100,000 anonymized rows on the target server. Record parse, transformation, and export time separately. The 50,000-row requirement passes only when end-to-end processing (excluding browser transfer) stays below 30 seconds.
