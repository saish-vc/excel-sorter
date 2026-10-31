# SheetSort Architecture

## Stack

Python 3.11+, Streamlit, pandas, openpyxl, SQLite, pytest, and Docker are retained. This is the smallest practical stack for a self-hosted college data tool: pandas handles tables efficiently, openpyxl produces formatted workbooks, and SQLite avoids operating a database server for a pilot.

~~~mermaid
flowchart LR
    B[College staff browser] --> S[Streamlit UI]
    S --> V[Validation and schema services]
    V --> P[pandas processing pipeline]
    P --> E[openpyxl Excel export]
    S <--> R[(SQLite Recipes)]
    S <--> A[(SQLite Audit Log)]
    E --> D[Downloaded XLSX report]
~~~

## Folder responsibilities

- app/main.py: Streamlit interaction and session state only.
- app/services/: upload, schema, cleaning, sorting, filtering, duplicate, split, recipe, and export logic.
- app/models/: typed dictionary contracts.
- app/utils/config.py: deployment-safe defaults.
- tests/: unit, integration, regression, and security-focused tests.
- sample_data/: anonymized demo data only.

## Pipeline and contracts

Upload -> Validate -> Detect schema -> Clean -> Sort -> Filter -> Deduplicate -> Split -> Summarize -> Export

Every transformation receives a DataFrame and returns a new DataFrame plus counts. Uploads are read in memory; Recipes and audit metadata are persisted in SQLite. Exports are newly generated workbooks, never changes to the uploaded file.

## Error policy

Empty, oversized, unsupported, unreadable, and corrupt files return plain-language errors. Missing columns and invalid rule values do not silently delete records. Ambiguous dates and near duplicates require review. Formula-like cell text is escaped during export to prevent spreadsheet formula injection.

## Privacy and deployment

Do not retain raw uploads. Restrict the SQLite database and log directory to the app account, put a shared deployment behind HTTPS and authentication, and agree retention/backup periods with the college before a live pilot. SQLite is appropriate for local/small-pilot use; move to a server database before high-concurrency college-wide deployment.
