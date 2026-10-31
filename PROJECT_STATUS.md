# SheetSort Project Status

**Last updated:** 31 October 2026
**Current state:** Complete runnable local Streamlit application with Windows desktop executable successfully built and tested.

## Completed

- Product requirements, personas, user stories, MVP scope, risks, and roadmap documented.
- Architecture, Mermaid diagram, processing pipeline, privacy guidance, QA/security guide, pilot/sales pack, and maintenance backlog documented.
- Streamlit workflow supports Excel/CSV upload, preview, schema detection, cleaning, sorting, filtering, duplicate handling, splitting, Recipes, audit-log viewing, and formatted Excel export.
- Recipes can be saved, loaded, updated, deleted, and applied.
- Exports include a Summary sheet and optional split sheets.
- Source uploads are processed in memory and never overwritten.
- Formula-like spreadsheet values are escaped during export.
- Unit and regression suite passes: **57 tests passed**.
- Local server smoke test passed: HTTP 200 at http://127.0.0.1:8501.
- Windows launcher, build script, and desktop-app guide added.
- **Windows desktop executable successfully built at dist\SheetSort\SheetSort.exe**.
- Desktop app tested: starts Streamlit server on 127.0.0.1:8501, health endpoint returns 'ok'.
- Fixed Python path resolution for both bundled (PyInstaller) and unbundled execution in main.py.
- Fixed sys.path handling in desktop_launcher.py for proper module imports.

## In progress

None.

## Remaining before a college production rollout

- Smoke-test the Windows executable on a clean Windows computer (not just the development machine).
- Code-sign the executable before broad distribution (prevents Windows Defender warnings).
- Define the college retention, backup, privacy, and access-control policies.
- Add login/role-based access if more than one staff member shares the deployment.
- Benchmark representative 1k, 10k, 50k, and 100k-row files on target hardware.
- Perform user-acceptance testing with Exam Cell, Placement, Attendance, and Administrator staff.
- Add dependency vulnerability scanning to the release pipeline.
- Decide whether to migrate from SQLite before a high-concurrency college-wide rollout.

## How to run

- Developer/local web mode: run Streamlit against sheetsort\app\main.py.
- Windows package: run build_windows.ps1, then distribute the full dist\SheetSort folder.

## Key documents

- STAGE_0_PRD.md
- docs\ARCHITECTURE.md
- docs\QA_AND_SECURITY.md
- docs\PILOT_AND_SALES.md
- docs\MAINTENANCE_AND_BACKLOG.md
- docs\WINDOWS_DESKTOP_APP.md
