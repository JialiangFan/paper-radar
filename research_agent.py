import arxiv
import openai
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime, timedelta
import os
import html
import time
import sqlite3
import schedule
from typing import List, Dict, Set, Optional

# --- 配置部分 ---
KEYWORDS_FILE = "keywords.txt"  # 关键词文件路径
MAX_RESULTS = 5  # 每次每个关键词抓几篇

def load_keywords() -> List[str]:
    """从文件读取关键词，每行一个关键词"""
    keywords = []
    default_keywords = ["Large Language Models", "Agentic Workflow"]  # 默认关键词
    
    try:
        if os.path.exists(KEYWORDS_FILE):
            with open(KEYWORDS_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    keyword = line.strip()
                    # 跳过空行和注释行（以#开头的行）
                    if keyword and not keyword.startswith('#'):
                        keywords.append(keyword)
            
            if keywords:
                print(f"✅ 从 {KEYWORDS_FILE} 读取了 {len(keywords)} 个关键词")
                return keywords
            else:
                print(f"⚠️  {KEYWORDS_FILE} 文件为空，使用默认关键词")
                return default_keywords
        else:
            print(f"⚠️  {KEYWORDS_FILE} 文件不存在，使用默认关键词")
            print(f"💡 提示：创建 {KEYWORDS_FILE} 文件，每行一个关键词，即可自定义搜索关键词")
            return default_keywords
    except Exception as e:
        print(f"❌ 读取关键词文件失败: {e}，使用默认关键词")
        return default_keywords
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") or "REDACTED_OPENAI_API_KEY" # 从环境变量获取，如果没有则使用默认值
EMAIL_SENDER = "REDACTED_EMAIL"
EMAIL_PASSWORD = "REDACTED_GMAIL_APP_PASSWORD"  # 应用专用密码，去掉空格
EMAIL_RECEIVER = "REDACTED_EMAIL"

# 验证必要的配置
if not OPENAI_API_KEY:
    raise ValueError("请设置环境变量 OPENAI_API_KEY")
if not EMAIL_SENDER:
    raise ValueError("请设置环境变量 EMAIL_SENDER")
if not EMAIL_PASSWORD:
    raise ValueError("请设置环境变量 EMAIL_PASSWORD")

# 初始化 OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# 数据库文件路径
DB_PATH = "papers.db"

def init_database():
    """初始化数据库，创建表结构"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建论文表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS papers (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            abstract TEXT,
            authors TEXT,
            date TEXT,
            summary TEXT,
            keyword TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            sent_at TIMESTAMP,
            UNIQUE(id)
        )
    """)
    
    # 创建索引以提高查询速度
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_paper_id ON papers(id)
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_paper_date ON papers(date)
    """)
    
    conn.commit()
    conn.close()
    print(f"✅ 数据库初始化完成: {DB_PATH}")

def is_paper_exists(paper_id: str) -> bool:
    """检查论文是否已存在于数据库中"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM papers WHERE id = ?", (paper_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def get_cached_summary(paper_id: str) -> Optional[str]:
    """从数据库获取缓存的总结"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT summary FROM papers WHERE id = ?", (paper_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result and result[0] else None

def save_paper(paper: Dict, summary: str, keyword: str, sent: bool = False):
    """保存论文到数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    sent_at = datetime.now().isoformat() if sent else None
    
    cursor.execute("""
        INSERT OR REPLACE INTO papers 
        (id, title, url, abstract, authors, date, summary, keyword, sent_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        paper['id'],
        paper['title'],
        paper['url'],
        paper['abstract'],
        paper['authors'],
        paper['date'],
        summary,
        keyword,
        sent_at
    ))
    
    conn.commit()
    conn.close()

def fetch_papers(keyword: str, days: int = 2, max_results: int = None) -> List[Dict]:
    """从 arXiv 获取最新论文，自动过滤已存在的论文
    
    Args:
        keyword: 搜索关键词
            - 用逗号分隔：使用 OR 逻辑（例如："chain-of-thought, PDDL planning"）
            - 用空格分隔：使用 AND 逻辑（例如："LLM reasoning"）
        days: 搜索过去多少天的论文（默认2天）
        max_results: 最大返回结果数（默认使用全局 MAX_RESULTS）
    """
    if max_results is None:
        max_results = MAX_RESULTS
    
    # 检查是否包含逗号（OR 逻辑）
    if ',' in keyword:
        # 用逗号分隔：使用 OR 逻辑
        # 例如："chain-of-thought, PDDL planning" → (chain-of-thought) OR (PDDL AND planning)
        parts = [part.strip() for part in keyword.split(',') if part.strip()]
        
        if len(parts) > 1:
            # 对每个部分，如果包含空格，则用 AND 连接
            or_queries = []
            for part in parts:
                keywords_in_part = part.split()
                if len(keywords_in_part) > 1:
                    # 这部分内部用 AND 连接
                    or_queries.append("(" + " AND ".join(keywords_in_part) + ")")
                else:
                    or_queries.append(part)
            
            query = " OR ".join(or_queries)
            print(f"🔍 搜索关键词: {keyword} (OR 模式: {query}, 过去 {days} 天, 最多 {max_results} 篇)...")
        else:
            query = keyword
            print(f"🔍 搜索关键词: {keyword} (过去 {days} 天, 最多 {max_results} 篇)...")
    else:
        # 没有逗号：用空格分隔，使用 AND 逻辑
        keywords_list = keyword.strip().split()
        if len(keywords_list) > 1:
            # 多个关键词：使用 AND 连接，确保所有关键词都出现
            query = " AND ".join(keywords_list)
            print(f"🔍 搜索关键词: {keyword} (AND 模式: {query}, 过去 {days} 天, 最多 {max_results} 篇)...")
        else:
            query = keyword
            print(f"🔍 搜索关键词: {keyword} (过去 {days} 天, 最多 {max_results} 篇)...")
    
    try:
        # 使用新的 Client API
        client_arxiv = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate # 按提交时间排序
        )
        
        papers = []
        new_count = 0
        cutoff_date = datetime.now().date() - timedelta(days=days)
        
        for result in client_arxiv.results(search):
            # 根据指定的天数过滤论文
            if result.published.date() >= cutoff_date:
                paper_id = result.entry_id
                
                # 检查是否已存在
                if is_paper_exists(paper_id):
                    print(f"  ⏭️  跳过已存在的论文: {result.title[:50]}...")
                    continue
                
                papers.append({
                    "title": result.title,
                    "url": result.entry_id,
                    "abstract": result.summary,
                    "authors": ", ".join([a.name for a in result.authors]),
                    "date": result.published.strftime("%Y-%m-%d"),
                    "id": paper_id
                })
                new_count += 1
        
        print(f"  ✅ 找到 {new_count} 篇新论文")
        return papers
    except Exception as e:
        print(f"❌ 获取论文失败 ({keyword}): {e}")
        return []

def summarize_paper(paper: Dict, keyword: str = "", max_retries: int = 3) -> str:
    """调用 LLM 进行中文总结，带缓存和重试机制"""
    # 先检查缓存
    cached_summary = get_cached_summary(paper['id'])
    if cached_summary:
        print(f"  💾 使用缓存的总结")
        return cached_summary
    
    # 缓存中没有，调用 API
    print(f"  🤖 调用 OpenAI API 生成总结...")
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
                model="gpt-5-nano-2025-08-07", # 使用指定的模型
                messages=[{"role": "user", "content": prompt}]
            )
            summary = response.choices[0].message.content
            # 保存到数据库（但不标记为已发送）
            save_paper(paper, summary, keyword, sent=False)
            return summary
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 指数退避
                print(f"  ⚠️  API 调用失败，{wait_time}秒后重试... ({e})")
                time.sleep(wait_time)
            else:
                print(f"  ❌ 总结论文失败 ({paper['title']}): {e}")
                error_summary = "总结生成失败，请查看原文。"
                # 即使失败也保存，避免重复尝试
                save_paper(paper, error_summary, keyword, sent=False)
                return error_summary

def send_email(content_html: str):
    """发送邮件"""
    msg = MIMEText(content_html, 'html', 'utf-8')
    msg['From'] = Header("Research Agent", 'utf-8')
    msg['To'] = Header(EMAIL_RECEIVER, 'utf-8')
    msg['Subject'] = Header(f"今日论文日报 - {datetime.now().strftime('%Y-%m-%d')}", 'utf-8')

    try:
        # Gmail SMTP 配置说明：
        # 1. 不能使用普通密码，必须使用"应用专用密码"（App Password）
        # 2. 获取方法：Google 账户 -> 安全性 -> 两步验证 -> 应用专用密码
        # 3. 如果没有开启两步验证，需要先开启
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, [EMAIL_RECEIVER], msg.as_string())
        server.quit()
        print("邮件发送成功")
    except Exception as e:
        print(f"邮件发送失败: {e}")
        raise

def main():
    """主函数：抓取论文、生成总结、发送邮件"""
    print("=" * 60)
    print(f"🚀 开始运行论文日报任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 初始化数据库
    init_database()
    
    # 从文件读取关键词
    keywords = load_keywords()
    print(f"📋 关键词列表: {', '.join(keywords)}\n")
    
    report_html = "<h1>今日 ArXiv 论文速递</h1>"
    has_updates = False
    seen_paper_ids: Set[str] = set()  # 用于跨关键词去重
    
    for keyword in keywords:
        # 默认搜索最近2天的论文（定时任务）
        papers = fetch_papers(keyword, days=2)
        if not papers:
            continue
            
        report_html += f"<h2>关键词: {html.escape(keyword)}</h2><hr>"
        
        for paper in papers:
            # 跨关键词去重：如果这篇论文已经处理过，跳过
            if paper['id'] in seen_paper_ids:
                continue
            seen_paper_ids.add(paper['id'])
            
            has_updates = True
            print(f"  📄 处理论文: {paper['title'][:60]}...")
            summary = summarize_paper(paper, keyword)
            
            # HTML 转义防止 XSS，拼接 HTML
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
            
            # 保存论文到数据库（标记为已发送）
            save_paper(paper, summary, keyword, sent=True)

    if has_updates:
        print(f"\n📧 发现 {len(seen_paper_ids)} 篇新论文，正在发送邮件...")
        send_email(report_html)
        print("✅ 任务完成！")
    else:
        print("\nℹ️  今天没有发现符合条件的新论文。")

def run_scheduled_task():
    """定时任务入口"""
    try:
        main()
    except Exception as e:
        print(f"❌ 任务执行失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import sys
    
    # 如果传入 'schedule' 参数，启动定时任务
    if len(sys.argv) > 1 and sys.argv[1] == 'schedule':
        print("⏰ 启动定时任务模式...")
        print("📅 每天 10:00 自动运行")
        print("按 Ctrl+C 退出\n")
        
        # 设置定时任务：每天10:00运行
        schedule.every().day.at("10:00").do(run_scheduled_task)
        
        # 立即运行一次（可选）
        print("🚀 立即运行一次...")
        run_scheduled_task()
        
        # 保持运行
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
    else:
        # 直接运行一次
        main()