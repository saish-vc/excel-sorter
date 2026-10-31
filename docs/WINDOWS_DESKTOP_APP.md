# SheetSort Windows Desktop App

SheetSort can be distributed as a local Windows application. The executable starts a private Streamlit server on the user's computer and opens SheetSort in the default browser. Student data stays on that computer; the server binds only to 127.0.0.1.

## Build

From the repository root in PowerShell, run build_windows.ps1.

The distributable is dist\SheetSort\SheetSort.exe. Distribute the entire dist\SheetSort folder as a ZIP file; users extract it and double-click SheetSort.exe.

## User data

Recipes and audit metadata are stored in %USERPROFILE%\SheetSort\recipes.db. The packaged app does not keep raw uploaded files. Windows Defender or a college endpoint-security tool may request approval for an unsigned internal executable; sign the executable before broad deployment.

## Release checklist

- Run the pytest suite.
- Build on a clean Windows machine matching the target architecture.
- Start SheetSort.exe, upload a sample file, export a report, and save a Recipe.
- Code-sign the EXE and ZIP/distribute the complete dist\SheetSort directory.
