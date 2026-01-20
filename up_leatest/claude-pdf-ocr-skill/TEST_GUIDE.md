# PDF OCR Skill Test Script

This script tests the PDF OCR skill functionality.

## Prerequisites
1. Umi-OCR service running locally on port 1234
2. Python dependencies installed: `pip install pymupdf requests`

## Usage
1. Place a test PDF file in the `input` directory
2. Run this script: `python test_skill.py`
3. Check the `output` directory for generated Markdown files

## Test Functions
- Service availability check
- PDF processing
- Output file generation
- File naming conventions