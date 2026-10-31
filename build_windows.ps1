$ErrorActionPreference = "Stop"

python -m pip install pyinstaller
python -m PyInstaller --noconfirm --clean --onedir --windowed --name SheetSort --add-data "sheetsort;sheetsort" --collect-all streamlit --collect-all pandas --collect-all openpyxl desktop_launcher.py

Write-Host "Created: dist\SheetSort\SheetSort.exe"
