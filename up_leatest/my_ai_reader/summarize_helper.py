import os
import re

def split_text_by_sentences(text, max_chars=5000):
    """按句号分割文本，每段不超过 max_chars 字符"""
    # 使用句号、感叹号、问号作为分割符
    sentences = re.split(r'[.!?。！？]', text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # 添加句号（除了最后一个句子）
        sentence_with_punct = sentence + '.' if sentence != sentences[-1] else sentence

        # 如果加上新句子超过限制，则保存当前块并开始新的块
        if len(current_chunk) + len(sentence_with_punct) > max_chars and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = sentence_with_punct
        else:
            current_chunk += sentence_with_punct

    # 添加最后一块（如果非空）
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks

def create_summary_template(chunk_text, chunk_index, total_chunks):
    """为单个文本块创建总结模板"""
    template = f"""# 文本块 {chunk_index + 1}/{total_chunks} 的分析

## 原始内容预览
```
{chunk_text[:500]}...
```

## 待填写的分析内容

### 1. 主要观点
- [在此处添加该部分的核心要点]

### 2. 关键操作
- [在此处提取文档中提到的重要步骤或操作方法]

### 3. 亮点句子
- [在此处挑选最有价值或最具启发性的句子]

### 4. 内容总结
[在此处用一段话概括这部分内容]

---
"""
    return template

def generate_summary_prompts(file_path, output_dir="summaries"):
    """为主文档的每个部分生成总结提示文件"""
    # 读取文件
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"错误：找不到文件 {file_path}")
        return
    except Exception as e:
        print(f"读取文件时出错: {str(e)}")
        return

    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 分割文本
    chunks = split_text_by_sentences(content)
    print(f"文档已分割为 {len(chunks)} 个部分")

    # 为每个部分生成总结模板
    for i, chunk in enumerate(chunks):
        print(f"正在为第 {i+1}/{len(chunks)} 部分生成总结模板...")
        template = create_summary_template(chunk, i, len(chunks))

        # 保存模板
        template_path = os.path.join(output_dir, f"summary_{i+1:03d}.md")
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(template)

    # 创建最终整合报告的模板
    final_template = f"""# 综合总结报告

> 基于对原始文档 {file_path} 的分段分析

## 1. 整体概述
[在此处描述文档的主要内容和目的]

## 2. 核心观点汇总
[在此处整合各部分的核心观点]

## 3. 操作指南汇总
[在此处汇总文档中涉及的关键操作步骤]

## 4. 精彩摘录
[在此处收集最有价值的句子]

## 5. 总结评价
[在此处对整个文档进行价值评估和应用建议]

---
*本报告基于对原始文档的 {len(chunks)} 个部分的分析整理而成*
"""

    final_path = os.path.join(output_dir, "final_summary.md")
    with open(final_path, 'w', encoding='utf-8') as f:
        f.write(final_template)

    print(f"已生成 {len(chunks)} 个总结模板和1个最终报告模板")
    print(f"请在 {output_dir} 目录中填写各个总结文件，然后将内容整合到最终报告中")
    return len(chunks)

# 使用示例
if __name__ == "__main__":
    # 将 "your_large_document.md" 替换为你要总结的实际文件路径
    input_file = "readme.md"  # 或者你提到的读本文档

    # 生成总结模板
    num_chunks = generate_summary_prompts(input_file)
    if num_chunks > 0:
        print(f"\n下一步操作：")
        print(f"1. 检查 summaries 目录中的 {num_chunks} 个 summary_*.md 文件")
        print(f"2. 逐一填写每个文件中的分析内容")
        print(f"3. 将各部分的关键信息整合到 summaries/final_summary.md 中")
        print(f"4. 完成后你将得到一份完整的综合总结报告")