"""完整功能测试 - 扩大时间范围以找到论文"""
import arxiv
import openai
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime, timedelta
import os
import html
import time
from typing import List, Dict, Set

# --- 配置部分 ---
KEYWORDS = ["Large Language Models", "Agentic Workflow"]
MAX_RESULTS = 3  # 测试时只抓 3 篇
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
EMAIL_SENDER = os.environ.get("EMAIL_SENDER", "")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")
EMAIL_RECEIVER = os.environ.get("EMAIL_RECEIVER", "")

# 初始化 OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def fetch_papers(keyword: str, days: int = 7) -> List[Dict]:
    """从 arXiv 获取最新论文（测试时扩大时间范围）"""
    print(f"🔍 搜索关键词: {keyword}...")
    try:
        client_arxiv = arxiv.Client()
        search = arxiv.Search(
            query=keyword,
            max_results=MAX_RESULTS,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        papers = []
        for result in client_arxiv.results(search):
            # 测试时扩大时间范围到7天
            if result.published.date() >= (datetime.now().date() - timedelta(days=days)):
                papers.append({
                    "title": result.title,
                    "url": result.entry_id,
                    "abstract": result.summary,
                    "authors": ", ".join([a.name for a in result.authors]),
                    "date": result.published.strftime("%Y-%m-%d"),
                    "id": result.entry_id
                })
        return papers
    except Exception as e:
        print(f"❌ 获取论文失败 ({keyword}): {e}")
        return []

def summarize_paper(paper: Dict, max_retries: int = 3) -> str:
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
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"⚠️  API 调用失败，{wait_time}秒后重试... ({e})")
                time.sleep(wait_time)
            else:
                print(f"❌ 总结论文失败 ({paper['title']}): {e}")
                return "总结生成失败，请查看原文。"

def test_full_workflow():
    """测试完整工作流程"""
    print("=" * 60)
    print("🧪 开始完整功能测试")
    print("=" * 60)
    
    report_html = "<h1>测试报告 - ArXiv 论文速递</h1>"
    has_updates = False
    seen_paper_ids: Set[str] = set()
    
    for keyword in KEYWORDS:
        papers = fetch_papers(keyword, days=7)  # 扩大时间范围到7天
        if not papers:
            print(f"  ⚠️  最近 7 天没有找到新论文")
            continue
            
        print(f"  ✅ 找到 {len(papers)} 篇论文")
        report_html += f"<h2>关键词: {html.escape(keyword)}</h2><hr>"
        
        for paper in papers:
            if paper['id'] in seen_paper_ids:
                continue
            seen_paper_ids.add(paper['id'])
            
            has_updates = True
            print(f"\n  📄 正在处理: {paper['title'][:60]}...")
            summary = summarize_paper(paper)
            print(f"  ✅ 总结完成")
            
            title_escaped = html.escape(paper['title'])
            authors_escaped = html.escape(paper['authors'])
            summary_escaped = html.escape(summary).replace('\n', '<br>')
            
            report_html += f"""
            <h3><a href="{paper['url']}">{title_escaped}</a></h3>
            <p><b>作者:</b> {authors_escaped} | <b>日期:</b> {paper['date']}</p>
            <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">
                {summary_escaped}
            </div>
            <br>
            """

    if has_updates:
        print("\n" + "=" * 60)
        print("📧 正在发送测试邮件...")
        print("=" * 60)
        
        msg = MIMEText(report_html, 'html', 'utf-8')
        msg['From'] = Header("Research Agent Test", 'utf-8')
        msg['To'] = Header(EMAIL_RECEIVER, 'utf-8')
        msg['Subject'] = Header(f"测试报告 - {datetime.now().strftime('%Y-%m-%d')}", 'utf-8')

        try:
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, [EMAIL_RECEIVER], msg.as_string())
            server.quit()
            print("✅ 测试邮件发送成功！请检查收件箱。")
        except Exception as e:
            print(f"❌ 邮件发送失败: {e}")
    else:
        print("\n" + "=" * 60)
        print("⚠️  最近 7 天没有找到符合条件的新论文")
        print("=" * 60)
    
    print("\n" + "=" * 60)
    print("✅ 完整功能测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    test_full_workflow()

