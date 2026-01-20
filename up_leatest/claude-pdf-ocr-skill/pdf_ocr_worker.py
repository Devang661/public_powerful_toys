import os
import fitz  # PyMuPDF
import requests
import base64
import json
import time
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

# ================= 配置区域 =================
# 1. 你的 PDF 文件夹路径
INPUT_FOLDER = r"input"
# 2. 转换后的 MD 文件保存路径
OUTPUT_FOLDER = r"output"
# 3. Umi-OCR 的本地接口地址
OCR_API_URL = "http://127.0.0.1:1234/api/ocr"
# 4. 并发处理的线程数
MAX_WORKERS = 3
# 5. 图片放大倍数（提高OCR识别准确率）
IMAGE_SCALE = 2.0
# 6. 服务验证图片路径
SERVICE_TEST_IMAGE = r"test_service.png"
# ===========================================

def ocr_image(image_bytes):
    """
    将图片字节流发送给 Umi-OCR 接口并获取文字
    """
    try:
        # 将图片转换为 Base64 编码
        b64_img = base64.b64encode(image_bytes).decode('utf-8')

        # 构造请求数据 (Umi-OCR 标准 API 格式)
        data = {
            "base64": b64_img,
            # 可选参数：可以在这里指定语言等，具体看 Umi-OCR 文档
            # "options": {"ocr.language": "chi_sim"}
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(OCR_API_URL, data=json.dumps(data), headers=headers, timeout=30)

        if response.status_code == 200:
            res_json = response.json()
            # Umi-OCR 返回的数据结构通常包含 code 和 data
            if res_json.get("code") == 100:
                # 提取识别到的文本块并拼接
                text_blocks = [item['text'] for item in res_json['data']]
                return "\n".join(text_blocks)
            else:
                print(f"API 返回错误: {res_json}")
                return ""
        else:
            print(f"HTTP 请求失败: {response.status_code}")
            return ""

    except requests.exceptions.ConnectionError:
        print("连接Umi-OCR服务失败，请确保服务已启动并监听在正确端口")
        return ""
    except requests.exceptions.Timeout:
        print("OCR请求超时")
        return ""
    except Exception as e:
        print(f"OCR 请求异常: {e}")
        return ""


def test_ocr_service():
    """
    测试OCR服务是否可用
    """
    if not os.path.exists(SERVICE_TEST_IMAGE):
        print("警告: 服务测试图片不存在，跳过服务验证")
        return True

    try:
        with open(SERVICE_TEST_IMAGE, "rb") as f:
            test_image_bytes = f.read()

        print("正在测试OCR服务...")
        result = ocr_image(test_image_bytes)

        if result is not None:
            print("✅ OCR服务测试通过")
            return True
        else:
            print("❌ OCR服务测试失败")
            return False

    except Exception as e:
        print(f"❌ OCR服务测试异常: {e}")
        return False

def process_pdf_page(args):
    """
    处理PDF单页：转图片 -> OCR
    """
    page, page_num, total_pages, pdf_name = args
    print(f"  - 正在处理 {pdf_name} 第 {page_num}/{total_pages} 页...")

    # 将 PDF 页面转为图片
    # matrix=fitz.Matrix(IMAGE_SCALE, IMAGE_SCALE) 表示放大，提高清晰度以利于 OCR
    pix = page.get_pixmap(matrix=fitz.Matrix(IMAGE_SCALE, IMAGE_SCALE))
    img_bytes = pix.tobytes("png")

    # 调用 OCR
    page_text = ocr_image(img_bytes)

    return page_num, page_text

def should_add_space(current_text, next_text):
    """
    判断是否需要在两段文本之间添加空格
    """
    if not current_text or not next_text:
        return False

    # 获取当前文本的最后一个字符
    last_char = current_text[-1]
    # 获取下一段文本的第一个字符
    first_char = next_text[0] if len(next_text) > 0 else ''

    # 如果当前文本末尾是标点符号，不需要添加空格
    if last_char in '.,;:!?。，；：！？':
        return False

    # 如果下一段文本开头是标点符号，不需要添加空格
    if first_char in '.,;:!?。，；：！？':
        return False

    # 其他情况添加空格
    return True

def extract_date_from_document_start(pages_text_dict):
    """
    从文档前几页的文本中提取日期
    """
    # 收集前几页的文本（最多前3页）
    combined_text = ""
    page_count = 0
    for page_num in sorted(pages_text_dict.keys()):
        if page_count >= 3:  # 只检查前3页
            break
        combined_text += pages_text_dict[page_num] + "\n"
        page_count += 1

    # 提取前10行文本用于日期检测
    lines = combined_text.split('\n')
    first_lines = '\n'.join(lines[:10])

    return extract_date_from_text(first_lines)


def process_pdf(pdf_path, output_path):
    """
    处理单个 PDF：转图片 -> OCR -> 保存 MD
    """
    pdf_name = os.path.basename(pdf_path)
    print(f"正在处理: {pdf_name}...")

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"无法打开PDF文件 {pdf_name}: {e}")
        return

    # 使用线程池并发处理页面
    pages_data = [(doc[i], i+1, len(doc), pdf_name) for i in range(len(doc))]

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # 提交所有任务
        future_to_page = {executor.submit(process_pdf_page, args): args[1] for args in pages_data}

        # 收集结果
        page_results = {}
        for future in as_completed(future_to_page):
            page_num, page_text = future.result()
            page_results[page_num] = page_text

    # 按顺序组装文本，连续页面间智能连接
    full_text = f"# {pdf_name}\n\n"

    # 存储所有页面的文本
    all_page_texts = []
    for page_num in sorted(page_results.keys()):
        page_text = page_results[page_num]
        all_page_texts.append(page_text)
        print(f"  - 完成第 {page_num} 页")

    # 智能连接页面文本
    connected_text = ""
    for i, page_text in enumerate(all_page_texts):
        if i == 0:
            # 第一页直接添加
            connected_text = page_text
        else:
            # 检查是否需要连接文本
            prev_text = connected_text
            current_text = page_text

            # 如果前一页文本不为空且末尾不是句号等结束符，则连接文本
            if prev_text and prev_text.strip():
                last_char = prev_text.strip()[-1]
                if last_char not in '.。！!？?':
                    # 需要智能连接，判断是否添加空格
                    if should_add_space(prev_text, current_text):
                        connected_text += " " + current_text
                    else:
                        connected_text += current_text
                else:
                    # 以句号结尾，另起一段
                    connected_text += "\n\n" + current_text
            else:
                connected_text += current_text

    # 添加连接后的文本到完整文档
    full_text += connected_text

    # 保存文件（除非output_path为None）
    if output_path is not None:
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_text)
            print(f"✅ 已保存: {output_path}")
        except Exception as e:
            print(f"保存文件失败 {output_path}: {e}")
    else:
        print("临时处理完成，未保存文件")

    return page_results

def extract_date_from_filename(filename):
    """
    从文件名中提取日期并格式化为YYYY-MM-DD
    例如: 251019 -> 2025-10-19
    """
    # 查找6位数字模式 (YYMMDD)
    date_pattern = r'(\d{2})(\d{2})(\d{2})'
    match = re.search(date_pattern, filename)

    if match:
        year = f"20{match.group(1)}"  # 假设年份是20XX年
        month = match.group(2)
        day = match.group(3)
        return f"{year}-{month}-{day}"

    return None


def get_all_pdf_files(root_folder):
    """
    递归获取目录及其子目录中的所有PDF文件
    """
    pdf_files = []
    other_files = []

    for root, dirs, files in os.walk(root_folder):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, root_folder)

            if file.lower().endswith(".pdf"):
                pdf_files.append((file_path, relative_path))
            else:
                # 记录其他类型的文件
                other_files.append((file_path, relative_path))

    return pdf_files, other_files


def get_output_path(input_relative_path, output_folder):
    """
    根据输入文件的相对路径创建对应的输出路径，保持目录结构
    """
    # 移除文件名，保留目录结构
    dir_structure = os.path.dirname(input_relative_path)
    # 创建对应的输出目录
    output_dir = os.path.join(output_folder, dir_structure)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir


def main():
    if not os.path.exists(INPUT_FOLDER):
        os.makedirs(INPUT_FOLDER)
        print(f"创建输入目录: {INPUT_FOLDER}")

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"创建输出目录: {OUTPUT_FOLDER}")

    # 测试OCR服务是否可用
    if not test_ocr_service():
        print("OCR服务不可用，程序退出")
        return

    # 递归获取所有PDF文件和其他文件
    pdf_files, other_files = get_all_pdf_files(INPUT_FOLDER)

    if not pdf_files:
        print("未找到任何PDF文件")
        return

    print(f"找到 {len(pdf_files)} 个PDF文件")

    # 统计信息
    processed_count = 0
    skipped_count = 0
    error_count = 0

    # 处理每个PDF文件
    for full_path, relative_path in pdf_files:
        filename = os.path.basename(relative_path)
        print(f"\n正在处理: {relative_path}...")

        # 保持目录结构的输出路径
        output_dir = get_output_path(relative_path, OUTPUT_FOLDER)

        # 智能命名：提取日期并格式化文件名
        # 首先尝试从文件名中提取日期
        date_str = extract_date_from_filename(filename)

        # 如果文件名中没有日期，则从文档内容中提取
        if not date_str:
            print(f"  文件名中未找到日期，尝试从文档内容中提取...")
            # 先进行OCR处理以获取文档内容
            page_results = process_pdf(full_path, None)  # 临时处理，不保存文件
            if page_results:
                date_str = extract_date_from_document_start(page_results)
                if date_str:
                    print(f"  从文档内容中提取到日期: {date_str}")

        # 生成文件名
        if date_str:
            # 移除原文件名中的日期部分
            clean_filename = re.sub(r'\d{6}', '', os.path.splitext(filename)[0])
            # 清理多余的字符
            clean_filename = re.sub(r'[：:_\-]', '', clean_filename).strip()
            # 生成新的文件名
            md_filename = f"{date_str}-{clean_filename}.md"
        else:
            # 如果没有找到日期，使用原始文件名
            md_filename = os.path.splitext(filename)[0] + ".md"

        output_path = os.path.join(output_dir, md_filename)

        # 检查是否已存在输出文件且大小不为0
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"  跳过已处理的文件: {md_filename}")
            skipped_count += 1
            continue

        # 正式处理PDF并保存
        try:
            process_pdf(full_path, output_path)
            processed_count += 1
        except Exception as e:
            print(f"  处理文件时出错: {e}")
            error_count += 1

    # 程序结束时的汇总报告
    print("\n" + "="*50)
    print("处理完成汇总报告:")
    print("="*50)
    print(f"总计PDF文件: {len(pdf_files)}")
    print(f"已处理文件: {processed_count}")
    print(f"跳过文件: {skipped_count}")
    print(f"处理错误: {error_count}")

    if other_files:
        print(f"\n发现 {len(other_files)} 个非PDF文件:")
        # 按文件类型分类统计
        file_types = {}
        for _, relative_path in other_files:
            ext = os.path.splitext(relative_path)[1].lower()
            if ext not in file_types:
                file_types[ext] = 0
            file_types[ext] += 1

        for ext, count in file_types.items():
            if ext == "":
                ext = "无扩展名文件"
            print(f"  {ext}: {count} 个文件")
        print("  提示: 上述文件未处理，如需处理请转换为PDF格式")

    print("="*50)
    print("所有PDF文件处理完成！")


def extract_date_from_text(text):
    """
    从文本中提取日期并格式化为YYYY-MM-DD
    支持格式: "2025年10月16日" 或 "25年10月23日"
    """
    if not text:
        return None

    # 查找类似 "2025年10月16日" 的格式
    pattern1 = r'(\d{4})年(\d{1,2})月(\d{1,2})日'
    match1 = re.search(pattern1, text)

    if match1:
        year = match1.group(1)
        month = match1.group(2).zfill(2)  # 补零
        day = match1.group(3).zfill(2)    # 补零
        return f"{year}-{month}-{day}"

    # 查找类似 "25年10月23日" 的格式
    pattern2 = r'(\d{2})年(\d{1,2})月(\d{1,2})日'
    match2 = re.search(pattern2, text)

    if match2:
        year = f"20{match2.group(1)}"  # 假设年份是20XX年
        month = match2.group(2).zfill(2)  # 补零
        day = match2.group(3).zfill(2)    # 补零
        return f"{year}-{month}-{day}"

    return None

if __name__ == "__main__":
    main()