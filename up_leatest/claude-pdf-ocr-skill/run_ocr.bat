@echo off
chcp 65001 >nul
TITLE PDF OCR Processing Tool

echo ========================================
echo        PDF OCR Automation Tool
echo ========================================
echo.

REM Check if main script exists
if not exist "pdf_ocr_worker.py" (
    echo Error: Main script file pdf_ocr_worker.py not found.
    echo Please ensure it is in the same directory as this batch file.
    echo.
    pause
    exit /b 1
)

REM Check input directory
if not exist "input" (
    echo Creating input directory...
    mkdir input
)

REM Check output directory
if not exist "output" (
    echo Creating output directory...
    mkdir output
)

echo Ready!
echo Please place your PDF files into the "input" folder.
echo Press any key to start processing...
echo.
pause

cls
echo ========================================
echo        PDF OCR Automation Tool
echo ========================================
echo.

REM Run main script
echo Processing PDF files, please wait...
echo.
python pdf_ocr_worker.py

echo.
echo ========================================
echo Processing complete!
echo Generated Markdown files are in the "output" directory.
echo ========================================
echo.
pause