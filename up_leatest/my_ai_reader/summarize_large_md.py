import os
import re
from openai import OpenAI

# 初始化 ModelScope API 客户端
client = OpenAI(
    api_key="ms-f8e33591-4d78-43eb-b9d6-af96883c3e2f",  # 替换为你的 ModelScope Access Token
    base_url="https://api-inference.modelscope.cn/v1/"
)

def split_text_by_sentences(text, max_chars=5000):
    """按句号分割文本，每段不超过 max_chars 字符"""
    # 使用句号、感叹号、问号作为分割符
    sentences = re.split(r'[.!?。！？]', text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # 添加句号（除了最后一个句子）
        sentence_with_punct = sentence + '.' if len(chunks) < len(sentences) - 1 else sentence

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

def summarize_chunk(chunk_text, chunk_index, total_chunks):
    """使用 AI 对单个文本块进行总结"""
    prompt = f"""
    你是一个专业的技术文档分析师。请分析以下文档片段并提供总结。

    文档片段 ({chunk_index + 1}/{total_chunks}):
    {chunk_text}

    请提供以下信息：
    1. 主要观点：列出该部分的核心要点（3-5点）
    2. 关键操作：提取文档中提到的重要步骤或操作方法
    3. 亮点句子：挑选出最有价值或最具启发性的句子（2-3句）
    4. 总结：用一段话概括这部分内容

    请以清晰、简洁的方式回答，使用中文。
    """

    try:
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-Coder-32B-Instruct",
            messages=[
                {
                    'role': 'system',
                    'content': '你是一个专业的技术文档分析师，擅长提取关键信息和总结。'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            temperature=0.3,
            max_tokens=1000
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"处理第 {chunk_index + 1} 块时出错: {str(e)}"

def combine_summaries(summaries):
    """将所有总结合并成最终文档"""
    combined_prompt = f"""
    你是一个专业的技术文档总结专家。以下是同一文档不同部分的分析总结，请将它们整合成一份完整的总结报告。

    各部分总结如下：
    {'='*50}
    {'='*50}.join([f"第{i+1}部分:\\n{summary}\\n\\n" for i, summary in enumerate(summaries)])

    请根据以上内容，生成一份结构化的完整总结报告，包括：
    1. 整体概述：文档的主要内容和目的
    2. 核心观点：整合后的最重要的几点发现
    3. 操作指南：文档中涉及的关键操作步骤汇总
    4. 精彩摘录：最有价值的句子集合
    5. 总结评价：对整个文档的价值评估和应用建议

    报告应条理清晰，重点突出，便于读者快速了解文档核心内容。使用 Markdown 格式输出。
    """

    try:
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-Coder-32B-Instruct",
            messages=[
                {
                    'role': 'system',
                    'content': '你是一个专业的技术文档总结专家，擅长整合信息并生成结构化报告。'
                },
                {
                    'role': 'user',
                    'content': combined_prompt
                }
            ],
            temperature=0.3,
            max_tokens=2000
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"合并总结时出错: {str(e)}"

def summarize_large_markdown(file_path, output_path=None):
    """主函数：处理大型 Markdown 文件并生成总结"""
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

    # 分割文本
    chunks = split_text_by_sentences(content)
    print(f"文档已分割为 {len(chunks)} 个部分")

    # 对每个部分进行总结
    summaries = []
    for i, chunk in enumerate(chunks):
        print(f"正在处理第 {i+1}/{len(chunks)} 部分...")
        summary = summarize_chunk(chunk, i, len(chunks))
        summaries.append(summary)

        # 可选：保存中间结果以防中断
        with open(f"temp_summary_{i+1}.md", 'w', encoding='utf-8') as f:
            f.write(f"# 第{i+1}部分总结\n\n{summary}\n")

    # 合并所有总结
    print("正在生成最终总结报告...")
    final_summary = combine_summaries(summaries)

    # 输出结果
    if output_path is None:
        output_path = "summary_report.md"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_summary)

    print(f"总结完成！报告已保存至 {output_path}")
    return final_summary

# 使用示例
if __name__ == "__main__":
    # 将 "your_large_document.md" 替换为你要总结的实际文件路径
    input_file = "readme.md"  # 或者你提到的读本文档
    output_file = "comprehensive_summary.md"

    result = summarize_large_markdown(input_file, output_file)
    if result:
        print("总结已完成！")