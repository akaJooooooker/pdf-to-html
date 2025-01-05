import fitz  # PyMuPDF
import os

# === 設定檔案路徑 ===
pdf_path = "./me.pdf"  # 輸入 PDF 文件
output_dir = "D:\\python生活工具\\pdf"     # 輸出文件夾
html_output = "output.html"  # 輸出的 HTML 文件

# === 創建輸出文件夾 ===
os.makedirs(output_dir, exist_ok=True)

# === 打開 PDF ===
doc = fitz.open(pdf_path)

# === 初始化 HTML 內容 ===
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PDF Content</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }
        h2 { color: #333; }
        img { max-width: 100%; height: auto; margin-bottom: 20px; }
        .page { margin-bottom: 40px; border-bottom: 1px solid #ddd; padding-bottom: 20px; }
    </style>
</head>
<body>
    <h1>Extracted PDF Content</h1>
"""

# === 提取每一頁的內容 ===
for page_num, page in enumerate(doc, start=1):
    html_content += f'<div class="page"><h2>Page {page_num}</h2>\n'

    # 提取文字
    text = page.get_text()
    if text.strip():  # 如果有文字內容
        text = text.replace('\n', '<br>')  # 先替換換行符
        html_content += f"<p>{text}</p>\n"

    # 提取圖片
    for img_index, img in enumerate(page.get_images(full=True), start=1):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        image_path = f"{output_dir}/page_{page_num}_img_{img_index}.{image_ext}"

        # 保存圖片到文件夾
        with open(image_path, "wb") as img_file:
            img_file.write(image_bytes)

        # 將圖片添加到 HTML
        html_content += f'<img src="{image_path}" alt="Page {page_num} Image {img_index}">\n'

    html_content += '</div>\n'  # 結束該頁內容



# === 關閉 PDF 文件 ===
doc.close()

# === 結束 HTML 內容 ===
html_content += """
</body>
</html>
"""

# === 保存 HTML 文件 ===
with open(html_output, "w", encoding="utf-8") as html_file:
    html_file.write(html_content)

print(f"HTML 文件已生成：{html_output}")
print(f"圖片和文字已保存到文件夾：{output_dir}")