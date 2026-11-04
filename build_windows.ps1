$ErrorActionPreference = "Stop"

Write-Host "=== Building SheetSort Desktop for Windows ==="

# Locate Streamlit package directory
$streamlit_dir = python -c "import importlib.util, pathlib; print(pathlib.Path(importlib.util.find_spec('streamlit').origin).parent)"
Write-Host "Streamlit directory: $streamlit_dir"

# Clean previous build artifacts
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist\SheetSort") { Remove-Item -Recurse -Force "dist\SheetSort" }

# Build standalone distribution directory
python -m PyInstaller `
    --noconfirm `
    --clean `
    --onedir `
    --windowed `
    --name SheetSort `
    --add-data "sheetsort;sheetsort" `
    --add-data "$streamlit_dir\static;streamlit\static" `
    --collect-all streamlit `
    --collect-all pandas `
    --collect-all openpyxl `
    desktop_launcher.py

# Create a convenient launcher batch script inside dist\SheetSort
$batContent = @"
@echo off
cd /d "%~dp0"
start "" "%~dp0SheetSort.exe"
"@
Set-Content -Path "dist\SheetSort\Run-SheetSort.bat" -Value $batContent

# Create a README for end users
$readmeContent = @"
SheetSort - College Data Processing Desktop App
===============================================

How to run:
1. Double-click 'SheetSort.exe' (or 'Run-SheetSort.bat').
2. Your default web browser will automatically open with the SheetSort application.
3. No Python installation or internet connection is required.

All recipes and audit logs are safely stored in your user profile:
%USERPROFILE%\SheetSort\
"@
Set-Content -Path "dist\SheetSort\README.txt" -Value $readmeContent

# Package as downloadable ZIP using fast python zip
$zipName = "SheetSort-v1.2-Windows.zip"
if (Test-Path $zipName) { Remove-Item -Force $zipName }
Write-Host "Creating $zipName..."
python -c "import shutil; shutil.make_archive('SheetSort-v1.2-Windows', 'zip', 'dist', 'SheetSort')"

Write-Host ""
Write-Host "=== Build Successful ==="
Write-Host "Folder: dist\SheetSort"
Write-Host "Downloadable Archive: $zipName"
