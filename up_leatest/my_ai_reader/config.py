#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration file for the Document Batch Summary Tool
文档批量总结工具配置文件
"""

# API Configuration
# API配置
API_CONFIG = {
    "api_key": "ms-f8e33591-4d78-43eb-b9d6-af96883c3e2f",  # ModelScope Access Token
    "base_url": "https://api-inference.modelscope.cn/v1/",
    "model": "Qwen/Qwen2.5-Coder-32B-Instruct"
}

# Chunk Processing Configuration
# 文档分块处理配置
CHUNK_CONFIG = {
    "max_chars": 5000,  # Maximum characters per chunk 每个块的最大字符数
    "split_pattern": r'[.!?。！？]'  # Sentence splitting pattern 句子分割模式
}

# AI Prompt Templates
# AI提示模板
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

# Processing Options
# 处理选项
PROCESSING_OPTIONS = {
    "temperature": 0.3,
    "max_tokens_chunk": 1000,
    "max_tokens_final": 2000,
    "delay_between_requests": 1  # Delay in seconds between API requests 请求之间的延迟（秒）
}

# Directory Configuration
# 目录配置
DIRECTORY_CONFIG = {
    "raw_docs_dir": "raw_doc",
    "processed_docs_dir": "processed_docs"
}