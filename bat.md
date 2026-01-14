
## run python CL

```

@echo off
cd /d "%~dp0"
python 00.py
pause

```

## html to  txt 
```

import os
from pathlib import Path
from bs4 import BeautifulSoup

# 获取脚本所在目录
script_dir = Path(__file__).parent.resolve()

# 查找所有 .html 和 .htm 文件
html_files = [
    f for f in script_dir.glob("*")
    if f.is_file() and f.suffix.lower() in ('.html', '.htm')
]

if not html_files:
    print("⚠️ 当前文件夹中没有找到 .html 或 .htm 文件。")
else:
    print(f"🔍 找到 {len(html_files)} 个 HTML 文件，开始转换...\n")
    converted = 0

    for html_path in html_files:
        txt_path = html_path.with_suffix('.txt')

        # 可选：跳过已存在的 .txt 文件（取消下一行注释即可启用）
        # if txt_path.exists():
        #     print(f"⏭️  跳过（已存在）: {txt_path.name}")
        #     continue

        try:
            # 读取 HTML
            with open(html_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')

            # 提取纯文本，保留段落换行
            text = soup.get_text(separator='\n', strip=True)

            # 写入 TXT
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(text)

            print(f"✅ 已转换: {html_path.name} → {txt_path.name}")
            converted += 1

        except Exception as e:
            print(f"❌ 转换失败 {html_path.name}: {e}")

    print(f"\n🎉 共成功转换 {converted} 个文件！")
```
