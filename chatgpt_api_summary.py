import os
from openai import OpenAI
import yaml

# 讀取配置檔案
def load_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# 使用配置
config = load_config('config.yaml')

client = OpenAI(api_key=config["api_key"])

# 讀取文章內容
def read_article(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def read_prompt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
    
# 發送請求到 ChatGPT API
def summarize_article(article_text,prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content":f"{article_text}"},
            ]
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        print(f"API 請求失敗: {e}")
        return None

# 主程式
if __name__ == '__main__':
    output_dir = 'web_crawl_output'  # 文章檔案路徑
    output_markdown_dir = 'chatgpt_output'  # Markdown 檔案儲存路徑
    os.makedirs(output_markdown_dir, exist_ok=True)  # 確保目錄存在

    for filename in os.listdir(output_dir):
        if filename.endswith('.txt'):
            article_path = os.path.join(output_dir, filename)
            article_text = read_article(article_path)
            
            article_prompt = read_prompt('Prompt_TC.txt')
            summary = summarize_article(article_text,article_prompt)
            
            if summary:
                # 將總結寫入 Markdown 檔案
                markdown_filename = os.path.splitext(filename)[0] + '.md'
                markdown_path = os.path.join(output_markdown_dir, markdown_filename)
                with open(markdown_path, 'w', encoding='utf-8') as md_file:
                    md_file.write(summary)