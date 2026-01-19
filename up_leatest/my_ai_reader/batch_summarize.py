import os
import re
import time
import shutil
from openai import OpenAI

# Import configuration
try:
    from config import API_CONFIG, CHUNK_CONFIG, PROMPTS, PROCESSING_OPTIONS, DIRECTORY_CONFIG
except ImportError:
    # Fallback configuration if config.py is not found
    API_CONFIG = {
        "api_key": "ms-f8e33591-4d78-43eb-b9d6-af96883c3e2f",
        "base_url": "https://api-inference.modelscope.cn/v1/",
        "model": "Qwen/Qwen2.5-Coder-32B-Instruct"
    }
    CHUNK_CONFIG = {
        "max_chars": 5000,
        "split_pattern": r'[.!?。！？]'
    }
    PROMPTS = {
        "chunk_analysis": """
You are a professional technical document analyst. Please analyze the following document fragment and provide a summary.

Document Name: {filename}
Document Fragment ({chunk_index}/{total_chunks}):
{chunk_text}

Please provide the following information:
1. Main Points: List the core points of this section (3-5 points)
2. Key Operations: Extract important steps or methods mentioned in the document
3. Highlighted Sentences: Select the most valuable or enlightening sentences (2-3 sentences)
4. Summary: Summarize this section in one paragraph

Please answer in a clear and concise manner, using Chinese.
""",
        "final_summary": """
You are a professional technical document summary expert. Below are analysis summaries of different parts of the same document. Please integrate them into a complete summary report.

Document Name: {filename}

Summaries of each part:
{combined_content}

Based on the above content, please generate a structured complete summary report, including:
1. Overall Overview: Main content and purpose of the document
2. Core Points: Most important findings after integration
3. Operational Guide: Summary of key operational steps involved in the document
4. Excellent Excerpts: Collection of the most valuable sentences
5. Summary Evaluation: Value assessment and application recommendations for the entire document

The report should be well-structured and highlight key points for readers to quickly understand the core content of the document. Output in Markdown format.
Please answer in a clear and concise manner, using Chinese.
"""
    }
    PROCESSING_OPTIONS = {
        "temperature": 0.3,
        "max_tokens_chunk": 1000,
        "max_tokens_final": 2000,
        "delay_between_requests": 1
    }
    DIRECTORY_CONFIG = {
        "raw_docs_dir": "raw_doc",
        "processed_docs_dir": "processed_docs"
    }

# Initialize ModelScope API client
client = OpenAI(
    api_key=API_CONFIG["api_key"],
    base_url=API_CONFIG["base_url"]
)

def split_text_by_sentences(text, max_chars=None):
    """Split text by sentences, each part not exceeding max_chars characters"""
    if max_chars is None:
        max_chars = CHUNK_CONFIG["max_chars"]

    # Use periods, exclamation marks, and question marks as separators
    sentences = re.split(CHUNK_CONFIG["split_pattern"], text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # Add punctuation (except for the last sentence)
        sentence_with_punct = sentence + '.' if sentence != sentences[-1] else sentence

        # If adding the new sentence exceeds the limit, save the current chunk and start a new one
        if len(current_chunk) + len(sentence_with_punct) > max_chars and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = sentence_with_punct
        else:
            current_chunk += sentence_with_punct

    # Add the last chunk (if not empty)
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks

def summarize_chunk_with_ai(chunk_text, chunk_index, total_chunks, filename):
    """Use AI to summarize a single text chunk"""
    prompt = PROMPTS["chunk_analysis"].format(
        filename=filename,
        chunk_index=chunk_index + 1,
        total_chunks=total_chunks,
        chunk_text=chunk_text
    )

    try:
        response = client.chat.completions.create(
            model=API_CONFIG["model"],
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a professional technical document analyst, skilled at extracting key information and summarizing.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            temperature=PROCESSING_OPTIONS["temperature"],
            max_tokens=PROCESSING_OPTIONS["max_tokens_chunk"]
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Error processing chunk {chunk_index + 1}: {str(e)}"

def combine_summaries_with_ai(summaries, filename):
    """Combine all summaries into a final document"""
    combined_content = "\n\n====================\n\n".join([f"Part {i+1}:\n{summary}" for i, summary in enumerate(summaries)])

    prompt = PROMPTS["final_summary"].format(
        filename=filename,
        combined_content=combined_content
    )

    try:
        response = client.chat.completions.create(
            model=API_CONFIG["model"],
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a professional technical document summary expert, skilled at integrating information and generating structured reports.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            temperature=PROCESSING_OPTIONS["temperature"],
            max_tokens=PROCESSING_OPTIONS["max_tokens_final"]
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Error combining summaries: {str(e)}"

def process_single_document(file_path, output_base_dir=None):
    """Process a single document and generate a summary"""
    if output_base_dir is None:
        output_base_dir = DIRECTORY_CONFIG["processed_docs_dir"]

    filename = os.path.basename(file_path)
    filename_without_ext = os.path.splitext(filename)[0]

    # Create output directory
    output_dir = os.path.join(output_base_dir, filename_without_ext)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Check if summary file already exists
    summary_file = os.path.join(output_dir, f"{filename_without_ext}_summary.md")
    if os.path.exists(summary_file):
        print(f"Document {filename} already has a summary file, skipping processing")
        return True

    print(f"Starting to process document: {filename}")

    # Read file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        return False
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return False

    # Split text
    chunks = split_text_by_sentences(content)
    print(f"Document has been split into {len(chunks)} parts")

    # Summarize each part
    summaries = []
    for i, chunk in enumerate(chunks):
        print(f"Processing part {i+1}/{len(chunks)}...")
        summary = summarize_chunk_with_ai(chunk, i, len(chunks), filename)
        summaries.append(summary)

        # Save intermediate results in case of interruption
        temp_filename = os.path.join(output_dir, f"temp_summary_{i+1:03d}.md")
        with open(temp_filename, 'w', encoding='utf-8') as f:
            f.write(f"# Summary of Part {i+1}\n\n{summary}\n")

        # Add delay to avoid API limits
        time.sleep(PROCESSING_OPTIONS["delay_between_requests"])

    # Combine all summaries
    print("Generating final summary report...")
    final_summary = combine_summaries_with_ai(summaries, filename)

    # Output results
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(final_summary)

    # Clean up temporary files
    for i in range(len(chunks)):
        temp_filename = os.path.join(output_dir, f"temp_summary_{i+1:03d}.md")
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

    print(f"Document {filename} summary completed! Report saved to {summary_file}")
    return True

def process_raw_documents(raw_doc_dir=None, output_base_dir=None):
    """Process all documents in the raw_doc folder"""
    if raw_doc_dir is None:
        raw_doc_dir = DIRECTORY_CONFIG["raw_docs_dir"]

    if output_base_dir is None:
        output_base_dir = DIRECTORY_CONFIG["processed_docs_dir"]

    if not os.path.exists(raw_doc_dir):
        print(f"Error: Raw document directory {raw_doc_dir} not found")
        return

    if not os.path.exists(output_base_dir):
        os.makedirs(output_base_dir)

    # Get all document files
    doc_files = []
    for file in os.listdir(raw_doc_dir):
        if file.endswith(('.md', '.txt')):  # Support Markdown and text files
            doc_files.append(os.path.join(raw_doc_dir, file))

    if not doc_files:
        print(f"No supported document files found in {raw_doc_dir} directory")
        return

    print(f"Found {len(doc_files)} documents to process")

    # Process each document
    for doc_file in doc_files:
        try:
            process_single_document(doc_file, output_base_dir)
        except Exception as e:
            print(f"Error processing document {doc_file}: {str(e)}")

    print("All documents processed!")

# Usage example
if __name__ == "__main__":
    import sys

    # Check for command line arguments
    if len(sys.argv) > 1:
        # Process specified single file
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            # Use the directory where the file is located as the base output directory
            base_dir = os.path.dirname(file_path) or "."
            process_single_document(file_path, base_dir)
        else:
            print(f"Error: File {file_path} not found")
    else:
        # Process all documents in the raw_doc folder
        process_raw_documents()