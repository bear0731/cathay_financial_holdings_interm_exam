import os
import requests
from bs4 import BeautifulSoup

# 定義要抓取的網址
urls = [
    "https://www.ithome.com.tw/news/152373",
    "https://www.ithome.com.tw/news/159391"
]

# 創建 output 資料夾（如果不存在）
output_dir = 'web_crawl_output'
os.makedirs(output_dir, exist_ok=True)

# 爬取每個網址的內容
for url in urls:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取標題
        header = soup.find('h1', class_='page-header')
        header_text = header.get_text(strip=True) if header else "無標題"

        # 提取內容摘要
        content_summary = soup.find('div', class_='content-summary')
        summary_text = content_summary.get_text(strip=True) if content_summary else "無摘要"

        # 提取主要內容
        content = soup.find('div', class_='content')
        content_text = content.get_text(strip=True) if content else "無內容"

        # 替換標題中的特殊字符以便用作檔案名稱
        safe_title = "".join(c for c in header_text if c.isalnum() or c in (" ", "_")).rstrip()
        file_name = os.path.join(output_dir, f"{safe_title}.txt")

        # 寫入檔案
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(f"網址: {url}\n")
            f.write(f"標題: {header_text}\n")
            f.write(f"摘要: {summary_text}\n")
            f.write(f"內容: {content_text}")
    else:
        print(f"無法訪問網址: {url}")