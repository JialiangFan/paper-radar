import arxiv
import openai
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime, timedelta
import os

# --- 配置部分 ---
KEYWORDS = ["Large Language Models", "Agentic Workflow"] # 你的关键词
MAX_RESULTS = 5  # 每次每个关键词抓几篇
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") # 从环境变量获取
EMAIL_SENDER = os.environ.get("EMAIL_USER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASS")
EMAIL_RECEIVER = "REDACTED_EMAIL"

# 初始化 OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def fetch_papers(keyword):
    """从 arXiv 获取最新论文"""
    print(f"Searching for: {keyword}...")
    search = arxiv.Search(
        query=keyword,
        max_results=MAX_RESULTS,
        sort_by=arxiv.SortCriterion.SubmittedDate # 按提交时间排序
    )
    
    papers = []
    for result in search.results():
        # 过滤掉太旧的论文（比如只看最近2天的），可根据需求调整
        if result.published.date() >= (datetime.now().date() - timedelta(days=2)):
            papers.append({
                "title": result.title,
                "url": result.entry_id,
                "abstract": result.summary,
                "authors": ", ".join([a.name for a in result.authors]),
                "date": result.published.strftime("%Y-%m-%d")
            })
    return papers

def summarize_paper(paper):
    """调用 LLM 进行中文总结"""
    prompt = f"""
    请阅读以下论文的标题和摘要，用中文简要总结。
    
    格式要求：
    1. **核心创新点**：一句话概括。
    2. **主要方法**：简述用了什么技术/模型。
    3. **结论/性能**：取得了什么效果。
    
    Title: {paper['title']}
    Abstract: {paper['abstract']}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini", # 使用便宜快速的模型
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def send_email(content_html):
    """发送邮件"""
    msg = MIMEText(content_html, 'html', 'utf-8')
    msg['From'] = Header("Research Agent", 'utf-8')
    msg['To'] = Header("Master", 'utf-8')
    msg['Subject'] = Header(f"今日论文日报 - {datetime.now().strftime('%Y-%m-%d')}", 'utf-8')

    try:
        # 以 Gmail 为例 (需要开启 App Password)
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, [EMAIL_RECEIVER], msg.as_string())
        server.quit()
        print("邮件发送成功")
    except Exception as e:
        print(f"邮件发送失败: {e}")

def main():
    report_html = "<h1>今日 ArXiv 论文速递</h1>"
    has_updates = False
    
    for keyword in KEYWORDS:
        papers = fetch_papers(keyword)
        if not papers:
            continue
            
        report_html += f"<h2>关键词: {keyword}</h2><hr>"
        
        for paper in papers:
            has_updates = True
            summary = summarize_paper(paper)
            # 拼接 HTML
            report_html += f"""
            <h3><a href="{paper['url']}">{paper['title']}</a></h3>
            <p><b>作者:</b> {paper['authors']} | <b>日期:</b> {paper['date']}</p>
            <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">
                {summary.replace('\n', '<br>')}
            </div>
            <br>
            """

    if has_updates:
        send_email(report_html)
    else:
        print("今天没有发现符合条件的新论文。")

if __name__ == "__main__":
    main()