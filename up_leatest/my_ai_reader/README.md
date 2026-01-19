# 文档批量总结工具 / Document Batch Summary Tool

[English version below](#english-version)

## 简介

这是一个自动化工具，用于处理大型文档并生成结构化总结报告。程序会将大型文档分割成适当大小的块，使用AI对每个块进行分析，然后将所有分析结果整合成一份完整的总结报告。

## 文件结构

```
项目根目录/
├── raw_doc/                  # 原始文档目录（将要处理的文档放在这里）
├── processed_docs/           # 处理后的文档目录（自动生成）
├── batch_summarize.py        # 主处理程序
├── stable_run_summary.bat    # Windows批处理启动文件（推荐使用）
├── config.py                 # 配置文件（Python格式）
├── config.json               # 配置文件（JSON格式，备选）
└── README.md                 # 本说明文件（双语）
```

## 使用方法

1. 将需要处理的文档（.md 或 .txt 格式）放入 `raw_doc` 目录
2. 双击运行 `stable_run_summary.bat` 文件
3. 程序会自动处理 `raw_doc` 目录中的所有文档
4. 处理结果将保存在 `processed_docs` 目录中，每个文档对应一个子目录

## 配置文件说明

程序支持两种配置文件格式：
1. `config.py` - Python格式配置文件（推荐）
2. `config.json` - JSON格式配置文件（备选）

配置文件包含以下设置：
- **API配置**：API密钥、基础URL和模型名称
- **文档分块配置**：最大字符数和句子分割模式
- **AI提示模板**：块分析和最终总结的提示词
- **处理选项**：温度参数、最大令牌数和请求延迟
- **目录配置**：原始文档目录和处理后文档目录

修改配置文件后，程序会自动使用新的设置。

## 处理流程

1. 程序会将大型文档按句号分割成约5000字符的块
2. 对每个块使用AI进行分析，提取：
   - 主要观点
   - 关键操作
   - 亮点句子
   - 内容总结
3. 将所有块的分析结果整合成完整的总结报告
4. 生成包含以下内容的Markdown格式报告：
   - 整体概述
   - 核心观点
   - 操作指南
   - 精彩摘录
   - 总结评价

## 特性

- 自动跳过已处理的文档
- 支持断点续传（临时文件会在处理完成后自动清理）
- 生成结构化的总结报告
- 支持多种文档格式（.md, .txt）
- 程序界面为英文，生成的总结内容为中文

## 注意事项

- 确保已安装Python环境
- 确保网络连接正常（需要访问AI API）
- 处理大型文档可能需要较长时间，请耐心等待

---

# English Version

## Introduction

This is an automated tool for processing large documents and generating structured summary reports. The program splits large documents into appropriately sized chunks, analyzes each chunk using AI, and then integrates all analysis results into a complete summary report.

## File Structure

```
Project Root/
├── raw_doc/                  # Raw document directory (place documents to be processed here)
├── processed_docs/           # Processed document directory (automatically generated)
├── batch_summarize.py        # Main processing program
├── stable_run_summary.bat    # Windows batch startup file (recommended)
├── config.py                 # Configuration file (Python format)
├── config.json               # Configuration file (JSON format, alternative)
└── README.md                 # This instruction file (bilingual)
```

## Usage

1. Place documents to be processed (.md or .txt format) into the `raw_doc` directory
2. Double-click to run the `stable_run_summary.bat` file
3. The program will automatically process all documents in the `raw_doc` directory
4. Processing results will be saved in the `processed_docs` directory, with each document corresponding to a subdirectory

## Configuration File Instructions

The program supports two configuration file formats:
1. `config.py` - Python format configuration file (recommended)
2. `config.json` - JSON format configuration file (alternative)

The configuration file contains the following settings:
- **API Configuration**: API key, base URL, and model name
- **Document Chunking Configuration**: Maximum characters and sentence splitting pattern
- **AI Prompt Templates**: Prompts for chunk analysis and final summary
- **Processing Options**: Temperature parameters, maximum tokens, and request delay
- **Directory Configuration**: Raw document directory and processed document directory

After modifying the configuration file, the program will automatically use the new settings.

## Processing Workflow

1. The program splits large documents into chunks of approximately 5000 characters by periods
2. Analyzes each chunk using AI to extract:
   - Main points
   - Key operations
   - Highlighted sentences
   - Content summary
3. Integrates all chunk analysis results into a complete summary report
4. Generates a Markdown format report containing:
   - Overall overview
   - Core points
   - Operational guide
   - Excellent excerpts
   - Summary evaluation

## Features

- Automatically skips already processed documents
- Supports breakpoint resume (temporary files will be automatically cleaned up after processing)
- Generates structured summary reports
- Supports multiple document formats (.md, .txt)
- Program interface in English, generated summary content in Chinese

## Notes

- Ensure Python environment is installed
- Ensure network connection is normal (requires access to AI API)
- Processing large documents may take a long time, please be patient