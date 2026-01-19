@echo off

echo ========================================
echo Document Batch Summary Tool (Stable Version)
echo ========================================
echo.

:: Check Python environment
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python environment not found. Please install Python first.
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

:: Check required files
if not exist "batch_summarize.py" (
    echo Error: batch_summarize.py file not found.
    echo Please ensure the file is in the current directory.
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

:: Ensure necessary directories exist
if not exist "raw_doc" (
    echo Creating raw_doc directory...
    mkdir raw_doc
)
if not exist "processed_docs" (
    echo Creating processed_docs directory...
    mkdir processed_docs
)

echo.
echo Starting document processing...
echo.

:: Execute main program
python batch_summarize.py

echo.
echo ========================================
echo Processing completed!
echo ========================================
echo.

:: Display results summary
if exist "processed_docs" (
    echo Processing results:
    dir processed_docs /ad /b
    echo.
)

echo Press any key to exit...
pause >nul
exit /b 0