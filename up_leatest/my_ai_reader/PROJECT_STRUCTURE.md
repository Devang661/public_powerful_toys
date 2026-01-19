# 项目结构说明 / Project Structure

[English version below](#english-version)

## 最终项目结构

```
文档批量总结工具/
├── raw_doc/                  # 原始文档目录
│   ├── ai_introduction.md    # 示例文档
│   └── ...                   # 其他待处理文档
├── processed_docs/           # 处理后的文档目录
│   ├── ai_introduction/      # ai_introduction.md的处理结果
│   │   └── ai_introduction_summary.md  # 总结报告
│   └── ...                   # 其他文档的处理结果
├── batch_summarize.py        # 主处理程序 (英文界面，中文总结)
├── stable_run_summary.bat    # 启动批处理文件 (英文界面)
├── auto_summarize.py         # 自动总结程序 (备用)
├── summarize_large_md.py      # 大型Markdown文件处理程序 (备用)
├── summarize_helper.py        # 辅助处理程序 (备用)
├── ai.txt                    # AI配置示例文件
├── comprehensive_summary.md  # 综合总结示例
├── PROJECT_STRUCTURE.md      # 本项目结构说明文件
└── README.md                 # 双语使用说明
```

## 文件说明

### 核心文件
- **`batch_summarize.py`**: 主处理程序，负责文档分割、AI分析和结果整合
- **`stable_run_summary.bat`**: 推荐使用的启动文件，简单稳定

### 辅助文件
- **`auto_summarize.py`**: 自动总结程序，用于特定场景
- **`summarize_large_md.py`**: 专为大型Markdown文件设计的处理程序
- **`summarize_helper.py`**: 辅助处理程序，提供额外功能

### 配置和说明文件
- **`ai.txt`**: AI API配置示例
- **`README.md`**: 双语使用说明文档
- **`PROJECT_STRUCTURE.md`**: 项目结构说明文件

### 目录
- **`raw_doc/`**: 存放待处理的原始文档
- **`processed_docs/`**: 存放处理完成的总结报告

---

# English Version

## Final Project Structure

```
Document Batch Summary Tool/
├── raw_doc/                  # Raw document directory
│   ├── ai_introduction.md    # Sample document
│   └── ...                   # Other documents to process
├── processed_docs/           # Processed document directory
│   ├── ai_introduction/      # Processing results for ai_introduction.md
│   │   └── ai_introduction_summary.md  # Summary report
│   └── ...                   # Processing results for other documents
├── batch_summarize.py        # Main processing program (English interface, Chinese summary)
├── stable_run_summary.bat    # Startup batch file (English interface)
├── auto_summarize.py         # Auto summary program (backup)
├── summarize_large_md.py      # Large Markdown file processing program (backup)
├── summarize_helper.py        # Helper processing program (backup)
├── ai.txt                    # AI configuration sample file
├── comprehensive_summary.md  # Comprehensive summary example
├── PROJECT_STRUCTURE.md      # This project structure documentation
└── README.md                 # Bilingual usage instructions
```

## File Descriptions

### Core Files
- **`batch_summarize.py`**: Main processing program, responsible for document splitting, AI analysis, and result integration
- **`stable_run_summary.bat`**: Recommended startup file, simple and stable

### Auxiliary Files
- **`auto_summarize.py`**: Auto summary program, for specific scenarios
- **`summarize_large_md.py`**: Processing program designed specifically for large Markdown files
- **`summarize_helper.py`**: Helper processing program, providing additional features

### Configuration and Documentation Files
- **`ai.txt`**: AI API configuration sample
- **`README.md`**: Bilingual usage instructions
- **`PROJECT_STRUCTURE.md`**: Project structure documentation

### Directories
- **`raw_doc/`**: Store raw documents to be processed
- **`processed_docs/`**: Store completed summary reports