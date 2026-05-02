import arxiv
import openai
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime, timedelta
import os
import sys
import html
import time
import sqlite3
from typing import List, Dict, Set, Optional
import requests

# --- 配置部分 ---
KEYWORDS_FILE = "keywords.txt"  # 关键词文件路径
MAX_RESULTS = 5  # 每次每个关键词抓几篇
ENV_FILE = ".env"  # 环境变量文件路径

def load_env_file(env_path: str = ENV_FILE):
    """从 .env 文件加载环境变量"""
    env_file = os.path.join(os.path.dirname(__file__), env_path)
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 跳过空行和注释
                if not line or line.startswith('#'):
                    continue
                # 解析 KEY=VALUE 格式
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    # 只设置未存在的环境变量（环境变量优先级更高）
                    if key and value and key not in os.environ:
                        os.environ[key] = value
        print(f"✅ 已加载环境变量文件: {env_file}")
    else:
        print(f"⚠️  环境变量文件不存在: {env_file}，使用系统环境变量")

# 加载 .env 文件
load_env_file()

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
def _normalize_env(value: str, default: str) -> str:
    """轻量工具，确保环境名称统一为小写并带默认值"""
    normalized = (value or default).strip().lower()
    return normalized or default


def _detect_test_env_hint() -> Optional[str]:
    """检测是否处于测试场景（pytest 或 test_*.py 脚本）"""
    if os.environ.get("PYTEST_CURRENT_TEST"):
        return "test"

    argv = [os.path.basename(arg or "") for arg in sys.argv]
    if argv and argv[0] and argv[0].startswith("pytest"):
        return "test"
    if any(arg.startswith("pytest") for arg in argv[1:]):
        return "test"

    script_name = argv[0] if argv else ""
    if script_name.startswith("test_"):
        return "development"
    return None


def _resolve_app_env() -> str:
    """根据环境变量和运行场景推断 APP_ENV"""
    env_value = os.environ.get("APP_ENV", "production")
    normalized = _normalize_env(env_value, "production")
    hint = _detect_test_env_hint()

    if hint and normalized in {"production", "prod"}:
        print(f"🧪 检测到测试环境，自动使用 {hint} 数据库")
        normalized = hint
        os.environ["APP_ENV"] = normalized

    return normalized


# 运行环境（production/dev/test...）
APP_ENV = _resolve_app_env()

# 数据库路径：可通过 DATABASE_PATH 覆盖，否则根据环境自动切换
DB_PATH = os.environ.get("DATABASE_PATH")
if not DB_PATH:
    DEFAULT_DB_MAP = {
        "production": "papers.db",
        "prod": "papers.db",
        "development": "papers.dev.db",
        "dev": "papers.dev.db",
        "test": "papers.test.db",
    }
    DB_PATH = DEFAULT_DB_MAP.get(APP_ENV, "papers.db")

# 输出一次，方便区分不同环境使用的数据库
print(f"💾 当前运行环境: {APP_ENV}，数据库: {DB_PATH}")

# 从环境变量读取配置（优先级：系统环境变量 > .env 文件 > 默认值）
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
EMAIL_SENDER = os.environ.get("EMAIL_SENDER", "")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")
EMAIL_RECEIVER = os.environ.get("EMAIL_RECEIVER", "")
# SMTP服务器配置（如果使用SMTP）
SMTP_SERVER = os.environ.get("SMTP_SERVER", "localhost")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "25"))
SMTP_USE_SSL = os.environ.get("SMTP_USE_SSL", "false").lower() == "true"
SMTP_USE_TLS = os.environ.get("SMTP_USE_TLS", "true").lower() == "true"
EMAIL_SENDER_NAME = os.environ.get("EMAIL_SENDER_NAME", "Research Agent")

# Mailgun API配置
MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY", "")
MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN", "")
USE_MAILGUN_API = os.environ.get("USE_MAILGUN_API", "false").lower() == "true"

# 验证必要的配置
if not OPENAI_API_KEY:
    raise ValueError("请设置环境变量 OPENAI_API_KEY")
if not EMAIL_SENDER:
    raise ValueError("请设置环境变量 EMAIL_SENDER")
# EMAIL_PASSWORD 是可选的（本地SMTP服务器通常不需要认证）

# 初始化 OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def init_database():
    """初始化数据库，创建表结构（含 subscribers→users 迁移）"""
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

    # --- 迁移 subscribers → users ---
    # 检查旧表是否存在
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='subscribers'")
    has_subscribers = cursor.fetchone() is not None

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    has_users = cursor.fetchone() is not None

    if has_subscribers and not has_users:
        print("🔄 迁移 subscribers 表到 users 表...")
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                name TEXT DEFAULT '',
                lang TEXT DEFAULT 'zh',
                status TEXT DEFAULT 'active',
                token TEXT NOT NULL UNIQUE,
                email_frequency TEXT DEFAULT 'daily',
                last_sent_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                unsubscribed_at TIMESTAMP
            )
        """)
        cursor.execute("""
            INSERT INTO users (id, email, name, lang, status, token, email_frequency, created_at, unsubscribed_at)
            SELECT id, email, '', lang, status, token, 'daily', created_at, unsubscribed_at
            FROM subscribers
        """)
        cursor.execute("DROP TABLE subscribers")
        print("✅ 迁移完成")

    if not has_users and not has_subscribers:
        # 全新安装
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                name TEXT DEFAULT '',
                lang TEXT DEFAULT 'zh',
                status TEXT DEFAULT 'active',
                token TEXT NOT NULL UNIQUE,
                email_frequency TEXT DEFAULT 'daily',
                last_sent_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                unsubscribed_at TIMESTAMP
            )
        """)

    # 创建 user_keywords 表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            keyword TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE(user_id, keyword)
        )
    """)

    # 创建索引
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_email ON users(email)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_token ON users(token)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_keywords_user_id ON user_keywords(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_paper_keyword ON papers(keyword)")

    conn.commit()
    conn.close()
    print(f"✅ 数据库初始化完成: {DB_PATH}")


# --- 用户相关辅助函数 ---

def get_active_users() -> List[Dict]:
    """获取所有活跃用户"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE status = 'active'")
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return users


def get_user_keywords(user_id: int) -> List[str]:
    """获取用户的关键词列表"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT keyword FROM user_keywords WHERE user_id = ? ORDER BY id", (user_id,))
    keywords = [row[0] for row in cursor.fetchall()]
    conn.close()
    return keywords


def should_send_to_user(user: Dict, now: datetime) -> bool:
    """根据用户的邮件频率判断是否应该发送"""
    frequency = user.get('email_frequency', 'daily')
    last_sent = user.get('last_sent_at')

    if not last_sent:
        return True  # 从未发送过，立即发送

    if isinstance(last_sent, str):
        try:
            last_sent = datetime.fromisoformat(last_sent)
        except ValueError:
            return True

    delta = now - last_sent
    if frequency == 'daily':
        return delta.total_seconds() >= 20 * 3600  # 20小时（容忍时间漂移）
    elif frequency == 'every_3_days':
        return delta.days >= 3
    elif frequency == 'weekly':
        return delta.days >= 7
    return True


def update_user_last_sent(user_id: int):
    """更新用户的最后发送时间"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET last_sent_at = ? WHERE id = ?",
        (datetime.now().isoformat(), user_id)
    )
    conn.commit()
    conn.close()

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

def get_recent_papers_from_db(days: int = 7, limit: int = 10) -> List[Dict]:
    """从数据库获取最近N天内已发送的论文（用于回顾）"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

    cursor.execute("""
        SELECT id, title, url, abstract, authors, date, summary, keyword
        FROM papers
        WHERE sent_at IS NOT NULL
        AND date >= ?
        ORDER BY date DESC
        LIMIT ?
    """, (cutoff_date, limit))

    papers = []
    for row in cursor.fetchall():
        papers.append({
            'id': row[0],
            'title': row[1],
            'url': row[2],
            'abstract': row[3],
            'authors': row[4],
            'date': row[5],
            'summary': row[6],
            'keyword': row[7]
        })

    conn.close()
    return papers

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

def fetch_papers(keyword: str, days: int = 30, max_results: int = None) -> List[Dict]:
    """从 arXiv 获取最新论文，自动过滤已存在的论文
    
    Args:
        keyword: 搜索关键词
            - 用逗号分隔：使用 OR 逻辑（例如："chain-of-thought, PDDL planning"）
            - 用空格分隔：使用 AND 逻辑（例如："LLM reasoning"）
        days: 搜索过去多少天的论文（默认30天）
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

def fetch_papers_by_author(
    author: str,
    days: int = 30,
    max_results: int = None,
    deduplicate: bool = True,
) -> List[Dict]:
    """按作者从 arXiv 获取最新论文，自动过滤已存在的论文
    
    Args:
        author: 作者姓名（英文），例如 "Yann LeCun"
        days: 搜索过去多少天的论文（默认30天）
        max_results: 最大返回结果数（默认使用全局 MAX_RESULTS）
        deduplicate: 是否跳过数据库中已存在的论文
    """
    if max_results is None:
        max_results = MAX_RESULTS
    
    # 使用 arXiv 的作者查询语法 au:"Name"
    query = f'au:"{author}"'
    print(f"🔍 按作者搜索: {author} (query: {query}, 过去 {days} 天, 最多 {max_results} 篇)...")
    
    try:
        client_arxiv = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        papers = []
        new_count = 0
        cutoff_date = datetime.now().date() - timedelta(days=days)
        
        seen_ids: Set[str] = set()

        for result in client_arxiv.results(search):
            if result.published.date() >= cutoff_date:
                paper_id = result.entry_id
                
                if paper_id in seen_ids:
                    continue
                seen_ids.add(paper_id)

                # 检查是否已存在
                if deduplicate and is_paper_exists(paper_id):
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
        
        print(f"  ✅ 找到 {new_count} 篇作者相关的新论文")
        return papers
    except Exception as e:
        print(f"❌ 获取作者论文失败 ({author}): {e}")
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

def send_email(content_html: str, subject: str = None, to: str = None):
    """发送邮件 - 支持Mailgun API和SMTP两种方式

    Args:
        content_html: HTML格式的邮件内容
        subject: 邮件主题（可选，默认使用今日论文日报）
        to: 收件人邮箱（可选，默认使用 EMAIL_RECEIVER）
    """
    if subject is None:
        subject = f"今日论文日报 - {datetime.now().strftime('%Y-%m-%d')}"
    if to is None:
        to = EMAIL_RECEIVER

    # 如果配置了使用Mailgun API，优先使用Mailgun
    if USE_MAILGUN_API and MAILGUN_API_KEY and MAILGUN_DOMAIN:
        try:
            return send_email_via_mailgun(content_html, subject, to=to)
        except Exception as e:
            print(f"Mailgun API发送失败，尝试使用SMTP: {e}")

    # 使用SMTP发送
    try:
        return send_email_via_smtp(content_html, subject, to=to)
    except Exception as e:
        print(f"邮件发送失败: {e}")
        raise

def send_email_via_mailgun(content_html: str, subject: str, to: str = None):
    """使用Mailgun API发送邮件"""
    if not MAILGUN_API_KEY:
        raise ValueError("MAILGUN_API_KEY 未设置")
    if not MAILGUN_DOMAIN:
        raise ValueError("MAILGUN_DOMAIN 未设置")
    if to is None:
        to = EMAIL_RECEIVER

    url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"

    data = {
        "from": f"{EMAIL_SENDER_NAME} <{EMAIL_SENDER}>",
        "to": to,
        "subject": subject,
        "html": content_html
    }

    response = requests.post(
        url,
        auth=("api", MAILGUN_API_KEY),
        data=data,
        timeout=30
    )

    if response.status_code == 200:
        result = response.json()
        print(f"邮件发送成功 (Mailgun → {to}, Message ID: {result.get('id', 'N/A')})")
        return True
    else:
        error_msg = f"Mailgun API错误: {response.status_code} - {response.text}"
        print(error_msg)
        raise Exception(error_msg)

def send_email_via_smtp(content_html: str, subject: str, to: str = None):
    """使用SMTP发送邮件"""
    if to is None:
        to = EMAIL_RECEIVER

    msg = MIMEText(content_html, 'html', 'utf-8')
    msg['From'] = Header(f"{EMAIL_SENDER_NAME} <{EMAIL_SENDER}>", 'utf-8')
    msg['To'] = Header(to, 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')

    if SMTP_USE_SSL:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    else:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        if SMTP_USE_TLS:
            server.starttls()

    if EMAIL_PASSWORD:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)

    server.sendmail(EMAIL_SENDER, [to], msg.as_string())
    server.quit()
    print(f"邮件发送成功 (SMTP → {to})")
    return True

def _build_paper_html(paper: Dict, summary: str) -> str:
    """生成单篇论文的 HTML 片段"""
    title_escaped = html.escape(paper['title'])
    authors_escaped = html.escape(paper.get('authors', ''))
    summary_escaped = html.escape(summary or '').replace('\n', '<br>')
    return f"""
    <h3><a href="{paper['url']}">{title_escaped}</a></h3>
    <p><b>作者:</b> {authors_escaped} | <b>日期:</b> {paper['date']}</p>
    <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">
        {summary_escaped}
    </div>
    <br>
    """


def _send_for_user(user: Dict, keywords: List[str]):
    """为单个用户搜索论文并发送邮件"""
    user_email = user['email']
    user_name = user.get('name', '')
    print(f"\n👤 处理用户: {user_name or user_email}")

    if not keywords:
        print(f"  ⚠️  用户没有关键词，跳过")
        return

    print(f"  📋 关键词: {', '.join(keywords)}")

    report_html = "<h1>今日 ArXiv 论文速递</h1>"
    has_updates = False
    seen_paper_ids: Set[str] = set()

    for keyword in keywords:
        papers = fetch_papers(keyword, days=30)
        if not papers:
            continue

        report_html += f"<h2>关键词: {html.escape(keyword)}</h2><hr>"

        for paper in papers:
            if paper['id'] in seen_paper_ids:
                continue
            seen_paper_ids.add(paper['id'])

            has_updates = True
            print(f"  📄 处理论文: {paper['title'][:60]}...")
            summary = summarize_paper(paper, keyword)
            report_html += _build_paper_html(paper, summary)
            save_paper(paper, summary, keyword, sent=True)

    if has_updates:
        print(f"  📧 发现 {len(seen_paper_ids)} 篇新论文，发送邮件到 {user_email}")
        send_email(report_html, to=user_email)
        update_user_last_sent(user['id'])
    else:
        print(f"  ℹ️  无新论文，尝试发送回顾...")
        review_papers = []
        for days in [7, 30, 90]:
            review_papers = get_recent_papers_from_db(days=days, limit=5)
            if review_papers:
                break

        if review_papers:
            review_html = f"<h1>📚 论文回顾 - {datetime.now().strftime('%Y-%m-%d')}</h1>"
            review_html += "<p><i>今日无新论文，为您回顾近期的精选论文：</i></p><hr>"
            for paper in review_papers:
                review_html += _build_paper_html(paper, paper.get('summary', ''))
            send_email(review_html, subject=f"论文回顾 - {datetime.now().strftime('%Y-%m-%d')}", to=user_email)
            update_user_last_sent(user['id'])
            print(f"  ✅ 论文回顾已发送到 {user_email}")
        else:
            print(f"  ⚠️  无可回顾的论文")


def get_papers_by_keywords(keywords: List[str], limit: int = 20, offset: int = 0) -> Dict:
    """根据关键词列表查询论文，支持分页"""
    if not keywords:
        return {"papers": [], "total": 0}

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    placeholders = ",".join("?" for _ in keywords)

    # 获取总数
    cursor.execute(
        f"SELECT COUNT(*) FROM papers WHERE keyword IN ({placeholders})",
        keywords,
    )
    total = cursor.fetchone()[0]

    # 获取分页数据
    cursor.execute(
        f"""SELECT id, title, url, abstract, authors, date, summary, keyword, created_at
            FROM papers WHERE keyword IN ({placeholders})
            ORDER BY created_at DESC LIMIT ? OFFSET ?""",
        keywords + [limit, offset],
    )
    papers = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return {"papers": papers, "total": total}


def main():
    """主函数：按用户遍历，抓取论文、生成总结、发送邮件"""
    print("=" * 60)
    print(f"🚀 开始运行论文日报任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    init_database()

    now = datetime.now()
    users = get_active_users()

    if users:
        print(f"👥 共有 {len(users)} 个活跃用户")
        for user in users:
            if not should_send_to_user(user, now):
                freq = user.get('email_frequency', 'daily')
                print(f"\n⏭️  跳过用户 {user['email']}（频率: {freq}，未到发送时间）")
                continue
            keywords = get_user_keywords(user['id'])
            _send_for_user(user, keywords)
    else:
        # 向后兼容：无用户时回退到 keywords.txt + EMAIL_RECEIVER
        print("ℹ️  无注册用户，回退到 keywords.txt + EMAIL_RECEIVER 模式")
        keywords = load_keywords()
        print(f"📋 关键词列表: {', '.join(keywords)}\n")

        report_html = "<h1>今日 ArXiv 论文速递</h1>"
        has_updates = False
        seen_paper_ids: Set[str] = set()

        for keyword in keywords:
            papers = fetch_papers(keyword, days=30)
            if not papers:
                continue
            report_html += f"<h2>关键词: {html.escape(keyword)}</h2><hr>"
            for paper in papers:
                if paper['id'] in seen_paper_ids:
                    continue
                seen_paper_ids.add(paper['id'])
                has_updates = True
                print(f"  📄 处理论文: {paper['title'][:60]}...")
                summary = summarize_paper(paper, keyword)
                report_html += _build_paper_html(paper, summary)
                save_paper(paper, summary, keyword, sent=True)

        if has_updates:
            print(f"\n📧 发现 {len(seen_paper_ids)} 篇新论文，正在发送邮件...")
            send_email(report_html)
            print("✅ 任务完成！")
        else:
            print("\nℹ️  今天没有发现新论文，尝试发送论文回顾...")
            review_papers = []
            for days in [7, 30, 90]:
                review_papers = get_recent_papers_from_db(days=days, limit=5)
                if review_papers:
                    break
            if review_papers:
                review_html = f"<h1>📚 论文回顾 - {datetime.now().strftime('%Y-%m-%d')}</h1>"
                review_html += "<p><i>今日无新论文，为您回顾近期的精选论文：</i></p><hr>"
                for paper in review_papers:
                    review_html += _build_paper_html(paper, paper.get('summary', ''))
                send_email(review_html, subject=f"论文回顾 - {datetime.now().strftime('%Y-%m-%d')}")
                print("✅ 论文回顾邮件已发送！")
            else:
                print("⚠️  数据库中也没有可回顾的论文。")

    print("\n" + "=" * 60)
    print("🏁 所有任务完成")
    print("=" * 60)

if __name__ == "__main__":
    # 直接运行一次，不再在脚本内部处理定时任务
    main()
