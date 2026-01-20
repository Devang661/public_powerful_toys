#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF OCR Skill Test Script
"""

import os
import sys

def test_skill():
    """Test the PDF OCR skill functionality."""
    print("PDF OCR Skill Test")
    print("=" * 30)

    # Check if required files exist
    required_files = [
        "pdf_ocr_worker.py",
        "run_ocr.bat",
        "SKILL.md"
    ]

    for file in required_files:
        if os.path.exists(file):
            print(f"✓ Found {file}")
        else:
            print(f"✗ Missing {file}")
            return False

    # Check directory structure
    required_dirs = ["input", "output"]
    for directory in required_dirs:
        if os.path.exists(directory) and os.path.isdir(directory):
            print(f"✓ Found {directory} directory")
        else:
            print(f"⚠ {directory} directory not found (will be created on first run)")

    # Check Python dependencies
    try:
        import fitz
        import requests
        print("✓ Required Python packages installed")
    except ImportError as e:
        print(f"✗ Missing Python package: {e}")
        return False

    print("\n" + "=" * 30)
    print("Skill setup verification complete!")
    print("To use the skill:")
    print("1. Place PDF files in the 'input' directory")
    print("2. Run 'run_ocr.bat' or 'python pdf_ocr_worker.py'")
    print("3. Check 'output' directory for results")

    return True

if __name__ == "__main__":
    test_skill()