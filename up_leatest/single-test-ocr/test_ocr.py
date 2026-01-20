import requests
import base64
import json
import os

# 配置
IMAGE_FILE = "1221.png"
OCR_URL = "http://127.0.0.1:1234/api/ocr"

def main():
    # 1. 检查图片是否存在
    if not os.path.exists(IMAGE_FILE):
        print(f"❌ 错误：找不到文件 {IMAGE_FILE}，请确认它和脚本在同一个文件夹。")
        return

    print(f"正在读取图片: {IMAGE_FILE} ...")

    # 2. 读取图片并转为 Base64
    with open(IMAGE_FILE, "rb") as f:
        img_data = f.read()
        b64_img = base64.b64encode(img_data).decode("utf-8")

    # 3. 发送请求给 Umi-OCR
    print("正在发送给 Umi-OCR ...")
    payload = {"base64": b64_img}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(OCR_URL, data=json.dumps(payload), headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 100: # 100 通常代表成功
                print("\n✅ 识别成功！内容如下：\n" + "-"*30)
                # 提取每一段文字并打印
                for item in result.get("data", []):
                    print(item.get("text", ""))
                print("-"*30)
            else:
                print(f"⚠️ API 返回异常: {result}")
        else:
            print(f"❌ HTTP 请求失败，状态码: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败：请检查 Umi-OCR 是否已开启，并且 HTTP 接口端口是 1234。")
    except Exception as e:
        print(f"❌ 发生未知错误: {e}")

if __name__ == "__main__":
    main()