# PDF OCR Skill

## Description
This skill converts PDF files to searchable Markdown documents using local OCR service. It processes PDF files by converting pages to images, performing OCR recognition, and compiling the results into structured Markdown files with intelligent text joining across pages.

## Features
- Converts PDF files to Markdown with preserved structure
- Local OCR processing for privacy and unlimited usage
- Batch processing of multiple PDF files
- Concurrent processing for improved performance
- Intelligent text joining across page boundaries
- Automatic file naming based on extracted dates
- Skip already processed files to avoid duplication
- Service availability verification before processing

## Dependencies
- Python 3.6+
- PyMuPDF (fitz)
- requests
- Umi-OCR service running locally on port 1234

## Usage Instructions

### Setup
1. Install required Python packages:
   ```
   pip install pymupdf requests
   ```

2. Download and install Umi-OCR:
   - Download from the Umi-OCR GitHub project page
   - Start the application and ensure HTTP interface is enabled (default port 1234)

### Configuration
Modify the configuration section in `pdf_ocr_worker.py`:
- INPUT_FOLDER: Path to directory containing PDF files
- OUTPUT_FOLDER: Path to save generated Markdown files
- OCR_API_URL: Umi-OCR local API endpoint
- MAX_WORKERS: Number of concurrent threads
- IMAGE_SCALE: Image scaling factor for better OCR accuracy
- SERVICE_TEST_IMAGE: Path to test image for service verification

### Running the Skill
Place PDF files in the input directory, then run:
```
python pdf_ocr_worker.py
```

Or use the provided batch file:
```
run_ocr.bat
```

## Input/Output
- Input: PDF files placed in the configured input directory
- Output: Markdown files saved in the configured output directory

## Error Handling
The skill includes comprehensive error handling for:
- Connection failures to OCR service
- Timeout during OCR requests
- File access errors
- Invalid PDF files
- Memory limitations during processing

## Performance Tips
- Adjust IMAGE_SCALE for better OCR accuracy on low-quality PDFs
- Modify MAX_WORKERS based on system resources
- For large batches, consider reducing concurrency to prevent resource exhaustion