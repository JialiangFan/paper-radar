"""
Web UI for Research Agent
提供关键词管理、论文搜索、管理后台和用户自服务的 Web 界面（基于 FastAPI）
"""
import csv
import hashlib
import io
import os
import re
import sqlite3
import secrets
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, Request, HTTPException, Cookie, Response
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr
import html as html_escape

from research_agent import (
    load_keywords,
    fetch_papers,
    fetch_papers_by_author,
    summarize_paper,
    init_database,
    is_paper_exists,
    get_cached_summary,
    save_paper,
    send_email,
    get_papers_by_keywords,
    DB_PATH,
)

# 从环境变量读取配置
EMAIL_SENDER = os.environ.get("EMAIL_SENDER", "")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "changeme")

# 生成一个稳定的 admin token（基于密码的哈希）
ADMIN_TOKEN = hashlib.sha256(f"research_agent_admin_{ADMIN_PASSWORD}".encode()).hexdigest()

app = FastAPI(title="Research Agent Web UI")
templates = Jinja2Templates(directory="templates")
KEYWORDS_FILE = "keywords.txt"


# --- Pydantic Models ---

class KeywordCreate(BaseModel):
    keyword: str

class SearchRequest(BaseModel):
    keyword: str
    time_range: str = "7"
    max_results: int = 10
    backup_email: Optional[str] = ""

class AuthorSearchRequest(BaseModel):
    author: str
    days: int = 30
    max_results: int = 10

class SubscribeRequest(BaseModel):
    email: EmailStr
    name: str = ""
    lang: str = "zh"
    email_frequency: str = "daily"
    keywords: List[str] = []

class LoginRequest(BaseModel):
    email: EmailStr

class AdminLoginRequest(BaseModel):
    password: str

class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    lang: Optional[str] = None
    email_frequency: Optional[str] = None
    status: Optional[str] = None

class KeywordPayload(BaseModel):
    keyword: str


# --- Helper functions ---

def save_keywords(keywords: List[str]):
    """保存关键词到文件"""
    try:
        with open(KEYWORDS_FILE, 'w', encoding='utf-8') as f:
            for keyword in keywords:
                if keyword.strip():
                    f.write(keyword.strip() + '\n')
        return True
    except Exception as e:
        print(f"保存关键词失败: {e}")
        return False

def get_papers_from_db(limit=50):
    """从数据库获取已保存的论文"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, url, abstract, authors, date, summary, keyword, sent_at, created_at
        FROM papers ORDER BY created_at DESC LIMIT ?
    """, (limit,))
    papers = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return papers

def verify_admin(admin_token: str = None):
    """验证管理员 token"""
    if not admin_token or admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="未授权访问")


# ============================================================
# 公开页面
# ============================================================

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """主页"""
    keywords = load_keywords()
    papers = get_papers_from_db(limit=20)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "keywords": keywords, "papers": papers},
    )

@app.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request):
    """管理后台页面"""
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/user/{token}", response_class=HTMLResponse)
def user_portal(request: Request, token: str):
    """用户自服务页面"""
    # 验证 token 有效性
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE token = ?", (token,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="无效的用户链接")
    conn.close()
    return templates.TemplateResponse("user_portal.html", {"request": request, "token": token})


# ============================================================
# 全局关键词 API（保留原有功能）
# ============================================================

@app.get("/api/keywords")
def get_keywords():
    keywords = load_keywords()
    return {"keywords": keywords}

@app.post("/api/keywords")
def add_keyword(payload: KeywordCreate):
    keyword = payload.keyword.strip()
    if not keyword:
        raise HTTPException(status_code=400, detail="关键词不能为空")
    keywords = load_keywords()
    if keyword in keywords:
        raise HTTPException(status_code=400, detail="关键词已存在")
    keywords.append(keyword)
    if save_keywords(keywords):
        return {"success": True, "message": "关键词添加成功", "keywords": keywords}
    raise HTTPException(status_code=500, detail="保存失败")

@app.delete("/api/keywords/{index}")
def delete_keyword(index: int):
    keywords = load_keywords()
    if 0 <= index < len(keywords):
        deleted = keywords.pop(index)
        if save_keywords(keywords):
            return {"success": True, "message": f"已删除关键词: {deleted}", "keywords": keywords}
        raise HTTPException(status_code=500, detail="保存失败")
    raise HTTPException(status_code=400, detail="索引无效")


# ============================================================
# 论文搜索 API（保留原有功能）
# ============================================================

@app.post("/api/search")
def search_papers(payload: SearchRequest):
    keyword = payload.keyword.strip()
    time_range = payload.time_range or "7"
    max_results = payload.max_results or 10
    backup_email = (payload.backup_email or "").strip()

    if not keyword:
        raise HTTPException(status_code=400, detail="关键词不能为空")

    time_range_map = {"7": 7, "30": 30, "90": 90, "180": 180}
    days = time_range_map.get(time_range, 7)
    max_results = min(max(int(max_results), 1), 100)

    try:
        init_database()
        papers = fetch_papers(keyword, days=days, max_results=max_results)

        time_range_text = {"7": "7天", "30": "1个月", "90": "3个月", "180": "6个月"}.get(time_range, "7天")

        if not papers:
            return {
                "success": True,
                "message": f"未找到新论文（关键词: {keyword}, 时间范围: 过去{time_range_text}）",
                "papers": [],
            }

        results = []
        for paper in papers:
            summary = summarize_paper(paper, keyword)
            save_paper(paper, summary, keyword, sent=False)
            results.append({
                'id': paper['id'], 'title': paper['title'], 'url': paper['url'],
                'abstract': paper['abstract'], 'authors': paper['authors'],
                'date': paper['date'], 'summary': summary
            })

        email_sent = False
        if backup_email:
            try:
                report_html = f"<h1>论文搜索结果 - {keyword}</h1>"
                report_html += f"<p><b>搜索时间:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>"
                report_html += f"<p><b>时间范围:</b> 过去{time_range_text}</p>"
                report_html += f"<p><b>找到论文:</b> {len(results)} 篇</p><hr>"

                for paper in results:
                    title_escaped = html_escape.escape(paper['title'])
                    authors_escaped = html_escape.escape(paper['authors'])
                    summary_escaped = html_escape.escape(paper['summary']).replace('\n', '<br>')
                    report_html += f"""
                    <h3><a href="{paper['url']}">{title_escaped}</a></h3>
                    <p><b>作者:</b> {authors_escaped} | <b>日期:</b> {paper['date']}</p>
                    <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">
                        {summary_escaped}
                    </div><br>
                    """

                email_subject = f"论文搜索结果 - {keyword} ({datetime.now().strftime('%Y-%m-%d')})"
                send_email(report_html, subject=email_subject, to=backup_email)
                email_sent = True
            except Exception as e:
                print(f"发送备份邮件失败: {e}")

        message = f"找到 {len(results)} 篇新论文（时间范围: 过去{time_range_text}, 限制: {max_results} 篇）"
        if email_sent:
            message += f"，已发送到 {backup_email}"

        return {"success": True, "message": message, "papers": results, "email_sent": email_sent}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")


@app.post("/api/search_by_author")
def search_papers_by_author(payload: AuthorSearchRequest):
    author = payload.author.strip()
    days = max(int(payload.days), 1)
    max_results = min(max(int(payload.max_results), 1), 100)

    if not author:
        raise HTTPException(status_code=400, detail="作者姓名不能为空")

    try:
        papers = fetch_papers_by_author(author, days=days, max_results=max_results, deduplicate=False)
        if not papers:
            return {"success": True, "message": f"未找到作者 {author} 在过去 {days} 天的论文", "papers": []}

        results = [
            {"id": p["id"], "title": p["title"], "url": p["url"],
             "abstract": p["abstract"], "authors": p["authors"], "date": p["date"]}
            for p in papers
        ]

        return {
            "success": True,
            "message": f"找到作者 {author} 在过去 {days} 天的 {len(results)} 篇论文（限制: {max_results} 篇）",
            "papers": results,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"作者搜索失败: {str(e)}")


@app.get("/api/papers")
def get_papers(limit: int = 50):
    papers = get_papers_from_db(limit=limit)
    return {"papers": papers}

@app.get("/api/papers/all")
def get_all_papers():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, url, abstract, authors, date, summary, keyword, sent_at, created_at
        FROM papers ORDER BY created_at DESC
    """)
    papers = [dict(row) for row in cursor.fetchall()]
    conn.close()

    keywords_count = {}
    for paper in papers:
        kw = paper.get("keyword", "N/A")
        keywords_count[kw] = keywords_count.get(kw, 0) + 1

    return {"papers": papers, "total": len(papers), "keywords_count": keywords_count}


@app.get("/api/papers/export/csv")
def export_papers_csv():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, authors, date, keyword, url, abstract, summary, created_at, sent_at
        FROM papers ORDER BY created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Title", "Authors", "Date", "Keyword", "URL", "Abstract", "Summary", "Created At", "Sent At"])
    for row in rows:
        writer.writerow([row["id"], row["title"], row["authors"], row["date"], row["keyword"],
                         row["url"], row["abstract"] or "", row["summary"] or "",
                         row["created_at"], row["sent_at"] or ""])

    output.seek(0)
    csv_content = "\ufeff" + output.getvalue()
    filename = f"papers_{datetime.now().strftime('%Y%m%d')}.csv"
    return StreamingResponse(
        iter([csv_content]),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )

@app.get("/api/papers/{paper_id}")
def get_paper_detail(paper_id: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, url, abstract, authors, date, summary, keyword, sent_at, created_at
        FROM papers WHERE id = ?
    """, (paper_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"paper": dict(row)}
    raise HTTPException(status_code=404, detail="论文不存在")


# ============================================================
# 订阅 API（改造为 users 表）
# ============================================================

@app.post("/api/login")
def login(payload: LoginRequest, request: Request):
    """Magic Link 登录 - 发送包含用户门户链接的邮件"""
    email = payload.email.strip().lower()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT token, name, lang FROM users WHERE email = ? AND status = 'active'", (email,))
    row = cursor.fetchone()
    conn.close()

    # 无论邮箱是否存在都返回相同消息（防止邮箱枚举）
    success_msg = "如果该邮箱已注册，登录链接将发送到您的邮箱。"

    if row:
        token, name, lang = row
        base_url = str(request.base_url).rstrip("/")
        portal_url = f"{base_url}/user/{token}"

        if lang == "en":
            subject = "Your Research Agent Login Link"
            body = f"""
            <div style="font-family:sans-serif;max-width:600px;margin:0 auto;padding:20px;">
                <h2>Hi {name or 'there'},</h2>
                <p>Click the link below to access your Research Agent portal:</p>
                <p style="margin:20px 0;">
                    <a href="{portal_url}" style="background:#4f46e5;color:white;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:600;">
                        Open My Portal
                    </a>
                </p>
                <p style="color:#666;font-size:14px;">Or copy this link: {portal_url}</p>
                <p style="color:#999;font-size:12px;">If you did not request this, please ignore this email.</p>
            </div>
            """
        else:
            subject = "Research Agent 登录链接"
            body = f"""
            <div style="font-family:sans-serif;max-width:600px;margin:0 auto;padding:20px;">
                <h2>您好{(' ' + name) if name else ''},</h2>
                <p>点击下方链接进入您的 Research Agent 个人门户：</p>
                <p style="margin:20px 0;">
                    <a href="{portal_url}" style="background:#4f46e5;color:white;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:600;">
                        进入我的门户
                    </a>
                </p>
                <p style="color:#666;font-size:14px;">或复制链接: {portal_url}</p>
                <p style="color:#999;font-size:12px;">如果您没有请求此邮件，请忽略。</p>
            </div>
            """

        try:
            send_email(body, subject=subject, to=email)
        except Exception as e:
            print(f"发送登录链接邮件失败: {e}")

    return {"success": True, "message": success_msg}


@app.post("/api/subscribe")
def subscribe(payload: SubscribeRequest, request: Request):
    """订阅 - 创建待验证用户，发送验证邮件"""
    email = payload.email.strip().lower()
    name = payload.name.strip()
    lang = payload.lang if payload.lang in ("zh", "en") else "zh"
    frequency = payload.email_frequency if payload.email_frequency in ("daily", "every_3_days", "weekly") else "daily"
    initial_keywords = [k.strip() for k in payload.keywords if k.strip()]

    if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, status, token FROM users WHERE email = ?", (email,))
    existing = cursor.fetchone()

    if existing:
        user_id, status, token = existing
        if status == "active":
            conn.close()
            return {"success": True, "message": "您已订阅", "token": token}
        else:
            # 重新生成 token，更新信息，保持 pending 状态
            token = secrets.token_urlsafe(32)
            cursor.execute(
                "UPDATE users SET status='pending', name=?, lang=?, email_frequency=?, token=?, unsubscribed_at=NULL WHERE id=?",
                (name, lang, frequency, token, user_id),
            )
            conn.commit()
    else:
        token = secrets.token_urlsafe(32)
        try:
            cursor.execute(
                "INSERT INTO users (email, name, lang, status, token, email_frequency) VALUES (?, ?, ?, 'pending', ?, ?)",
                (email, name, lang, token, frequency),
            )
            user_id = cursor.lastrowid
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            raise HTTPException(status_code=400, detail="Email already exists")

    # 添加初始关键词
    if initial_keywords:
        for kw in initial_keywords:
            try:
                cursor.execute("INSERT OR IGNORE INTO user_keywords (user_id, keyword) VALUES (?, ?)", (user_id, kw))
            except Exception:
                pass
        conn.commit()

    conn.close()

    # 发送验证邮件
    base_url = str(request.base_url).rstrip("/")
    verify_url = f"{base_url}/api/verify/{token}"

    if lang == "en":
        subject = "Verify your Research Agent subscription"
        body = f"""
        <div style="font-family:sans-serif;max-width:600px;margin:0 auto;padding:20px;">
            <h2>Hi {name or 'there'},</h2>
            <p>Thank you for subscribing to Research Agent! Please verify your email to activate paper updates:</p>
            <p style="margin:20px 0;">
                <a href="{verify_url}" style="background:#4f46e5;color:white;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:600;">
                    Verify My Email
                </a>
            </p>
            <p style="color:#666;font-size:14px;">Or copy this link: {verify_url}</p>
            <p style="color:#999;font-size:12px;">If you did not subscribe, please ignore this email.</p>
        </div>
        """
    else:
        subject = "验证您的 Research Agent 订阅"
        body = f"""
        <div style="font-family:sans-serif;max-width:600px;margin:0 auto;padding:20px;">
            <h2>您好{(' ' + name) if name else ''},</h2>
            <p>感谢订阅 Research Agent！请点击下方链接验证邮箱，激活论文推送功能：</p>
            <p style="margin:20px 0;">
                <a href="{verify_url}" style="background:#4f46e5;color:white;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:600;">
                    验证我的邮箱
                </a>
            </p>
            <p style="color:#666;font-size:14px;">或复制链接: {verify_url}</p>
            <p style="color:#999;font-size:12px;">如果您没有订阅，请忽略此邮件。</p>
        </div>
        """

    try:
        send_email(body, subject=subject, to=email)
    except Exception as e:
        print(f"发送验证邮件失败: {e}")

    return {"success": True, "message": "验证邮件已发送，请查收邮箱并点击链接完成激活。"}


@app.post("/api/unsubscribe")
def unsubscribe_by_email(payload: SubscribeRequest):
    email = payload.email.strip().lower()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, status FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return {"success": False, "message": "该邮箱未订阅"}

    user_id, status = row
    if status == "unsubscribed":
        conn.close()
        return {"success": True, "message": "已取消订阅"}

    cursor.execute(
        "UPDATE users SET status='unsubscribed', unsubscribed_at=? WHERE id=?",
        (datetime.now().isoformat(), user_id),
    )
    conn.commit()
    conn.close()
    return {"success": True, "message": "取消订阅成功"}


@app.get("/api/verify/{token}", response_class=HTMLResponse)
def verify_email(token: str):
    """验证邮箱，激活用户"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, lang, status FROM users WHERE token = ?", (token,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return HTMLResponse(
            content='<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Verification Failed</title>'
            '<style>body{font-family:sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;background:#f5f5f5;}'
            '.box{background:white;padding:40px;border-radius:10px;text-align:center;box-shadow:0 2px 10px rgba(0,0,0,0.1);}</style>'
            '</head><body><div class="box"><h2>Invalid Link</h2><p>The verification link is invalid or expired.</p></div></body></html>',
            status_code=404,
        )

    user_id, email, lang, status = row

    if status == "active":
        conn.close()
        portal_url = f"/user/{token}"
        if lang == "en":
            title, message = "Already Verified", "Your email is already verified."
        else:
            title, message = "已验证", "您的邮箱已完成验证。"
    else:
        cursor.execute("UPDATE users SET status='active' WHERE id=?", (user_id,))
        conn.commit()
        conn.close()
        portal_url = f"/user/{token}"
        if lang == "en":
            title, message = "Email Verified!", "Your subscription is now active. You will start receiving paper updates."
        else:
            title, message = "验证成功！", "您的订阅已激活，将开始接收论文推送。"

    return HTMLResponse(
        content=f'<!DOCTYPE html><html><head><meta charset="UTF-8"><title>{title}</title>'
        f'<style>body{{font-family:sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);}}'
        f'.box{{background:white;padding:40px 60px;border-radius:10px;text-align:center;box-shadow:0 4px 20px rgba(0,0,0,0.2);}}'
        f'h2{{color:#333;margin-bottom:15px;}}p{{color:#666;}}a{{display:inline-block;margin-top:15px;padding:10px 24px;background:#4f46e5;color:white;border-radius:8px;text-decoration:none;font-weight:600;}}'
        f'</style></head><body><div class="box"><h2>{title}</h2><p>{message}</p>'
        f'<a href="{portal_url}">{"Go to My Portal" if lang == "en" else "进入我的门户"}</a></div></body></html>',
        status_code=200,
    )


@app.get("/api/unsubscribe/{token}", response_class=HTMLResponse)
def unsubscribe(token: str, request: Request):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, lang FROM users WHERE token = ?", (token,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return HTMLResponse(
            content='<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Unsubscribe</title>'
            '<style>body{font-family:sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;background:#f5f5f5;}'
            '.box{background:white;padding:40px;border-radius:10px;text-align:center;box-shadow:0 2px 10px rgba(0,0,0,0.1);}</style>'
            '</head><body><div class="box"><h2>Invalid Link</h2><p>The unsubscribe link is invalid or expired.</p></div></body></html>',
            status_code=404,
        )

    user_id, email, lang = row
    cursor.execute(
        "UPDATE users SET status='unsubscribed', unsubscribed_at=? WHERE id=?",
        (datetime.now().isoformat(), user_id),
    )
    conn.commit()
    conn.close()

    if lang == "en":
        title, message, note = "Unsubscribed", "You have been unsubscribed from paper updates.", f"Email: {email}"
    else:
        title, message, note = "取消订阅成功", "您已成功取消论文更新订阅。", f"邮箱: {email}"

    return HTMLResponse(
        content=f'<!DOCTYPE html><html><head><meta charset="UTF-8"><title>{title}</title>'
        f'<style>body{{font-family:sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);}}'
        f'.box{{background:white;padding:40px 60px;border-radius:10px;text-align:center;box-shadow:0 4px 20px rgba(0,0,0,0.2);}}'
        f'h2{{color:#333;margin-bottom:15px;}}p{{color:#666;}}'
        f'</style></head><body><div class="box"><h2>{title}</h2><p>{message}</p>'
        f'<p style="font-size:12px;color:#999;">{note}</p></div></body></html>',
        status_code=200,
    )


# ============================================================
# 管理后台 API（密码保护）
# ============================================================

@app.post("/api/admin/login")
def admin_login(payload: AdminLoginRequest, response: Response):
    if payload.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="密码错误")
    response.set_cookie(key="admin_token", value=ADMIN_TOKEN, httponly=True, max_age=86400)
    return {"success": True, "token": ADMIN_TOKEN}

@app.get("/api/admin/dashboard")
def admin_dashboard(admin_token: Optional[str] = Cookie(None)):
    verify_admin(admin_token)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users WHERE status='active'")
    active_users = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM papers")
    total_papers = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM user_keywords")
    total_keywords = cursor.fetchone()[0]

    conn.close()
    return {
        "active_users": active_users,
        "total_users": total_users,
        "total_papers": total_papers,
        "total_keywords": total_keywords,
    }

@app.get("/api/admin/users")
def admin_list_users(admin_token: Optional[str] = Cookie(None)):
    verify_admin(admin_token)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
    users = [dict(row) for row in cursor.fetchall()]

    # 附加每个用户的关键词
    for user in users:
        cursor.execute("SELECT keyword FROM user_keywords WHERE user_id = ? ORDER BY id", (user['id'],))
        user['keywords'] = [row['keyword'] for row in cursor.fetchall()]

    conn.close()
    return {"users": users}

@app.get("/api/admin/users/{user_id}")
def admin_get_user(user_id: int, admin_token: Optional[str] = Cookie(None)):
    verify_admin(admin_token)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="用户不存在")

    user = dict(row)
    cursor.execute("SELECT keyword FROM user_keywords WHERE user_id = ? ORDER BY id", (user_id,))
    user['keywords'] = [r['keyword'] for r in cursor.fetchall()]
    conn.close()
    return {"user": user}

@app.put("/api/admin/users/{user_id}")
def admin_update_user(user_id: int, payload: UserUpdateRequest, admin_token: Optional[str] = Cookie(None)):
    verify_admin(admin_token)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    updates = []
    params = []
    if payload.name is not None:
        updates.append("name = ?")
        params.append(payload.name)
    if payload.lang is not None:
        updates.append("lang = ?")
        params.append(payload.lang)
    if payload.email_frequency is not None:
        updates.append("email_frequency = ?")
        params.append(payload.email_frequency)
    if payload.status is not None:
        updates.append("status = ?")
        params.append(payload.status)
        if payload.status == "unsubscribed":
            updates.append("unsubscribed_at = ?")
            params.append(datetime.now().isoformat())
        elif payload.status == "active":
            updates.append("unsubscribed_at = NULL")

    if not updates:
        conn.close()
        return {"success": True, "message": "无更新"}

    params.append(user_id)
    sql = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(sql, params)
    conn.commit()
    conn.close()
    return {"success": True, "message": "用户已更新"}

@app.delete("/api/admin/users/{user_id}")
def admin_delete_user(user_id: int, admin_token: Optional[str] = Cookie(None)):
    verify_admin(admin_token)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_keywords WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return {"success": True, "message": "用户已删除"}

@app.post("/api/admin/users/{user_id}/keywords")
def admin_add_user_keyword(user_id: int, payload: KeywordPayload, admin_token: Optional[str] = Cookie(None)):
    verify_admin(admin_token)
    keyword = payload.keyword.strip()
    if not keyword:
        raise HTTPException(status_code=400, detail="关键词不能为空")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO user_keywords (user_id, keyword) VALUES (?, ?)", (user_id, keyword))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="关键词已存在")
    conn.close()
    return {"success": True, "message": f"已添加关键词: {keyword}"}

@app.delete("/api/admin/users/{user_id}/keywords/{keyword}")
def admin_delete_user_keyword(user_id: int, keyword: str, admin_token: Optional[str] = Cookie(None)):
    verify_admin(admin_token)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_keywords WHERE user_id = ? AND keyword = ?", (user_id, keyword))
    conn.commit()
    conn.close()
    return {"success": True, "message": f"已删除关键词: {keyword}"}

@app.get("/api/admin/papers")
def admin_list_papers(admin_token: Optional[str] = Cookie(None)):
    verify_admin(admin_token)
    return get_all_papers()

@app.delete("/api/admin/papers/{paper_id:path}")
def admin_delete_paper(paper_id: str, admin_token: Optional[str] = Cookie(None)):
    verify_admin(admin_token)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM papers WHERE id = ?", (paper_id,))
    deleted = cursor.rowcount
    conn.commit()
    conn.close()

    if deleted == 0:
        raise HTTPException(status_code=404, detail="论文不存在")
    return {"success": True, "message": "论文已删除"}


# ============================================================
# 用户自服务 API（token 认证）
# ============================================================

def _get_user_by_token(token: str) -> dict:
    """通过 token 获取用户信息"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE token = ?", (token,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="无效的用户链接")
    user = dict(row)
    cursor.execute("SELECT keyword FROM user_keywords WHERE user_id = ? ORDER BY id", (user['id'],))
    user['keywords'] = [r['keyword'] for r in cursor.fetchall()]
    conn.close()
    return user

@app.get("/api/user/{token}/profile")
def user_get_profile(token: str):
    user = _get_user_by_token(token)
    # 不返回敏感字段
    return {
        "user": {
            "id": user["id"],
            "email": user["email"],
            "name": user["name"],
            "lang": user["lang"],
            "status": user["status"],
            "email_frequency": user["email_frequency"],
            "keywords": user["keywords"],
            "created_at": user["created_at"],
        }
    }

@app.put("/api/user/{token}/profile")
def user_update_profile(token: str, payload: UserUpdateRequest):
    user = _get_user_by_token(token)
    user_id = user["id"]

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    updates = []
    params = []
    if payload.name is not None:
        updates.append("name = ?")
        params.append(payload.name)
    if payload.lang is not None:
        updates.append("lang = ?")
        params.append(payload.lang)
    if payload.email_frequency is not None:
        updates.append("email_frequency = ?")
        params.append(payload.email_frequency)

    if updates:
        params.append(user_id)
        cursor.execute(f"UPDATE users SET {', '.join(updates)} WHERE id = ?", params)
        conn.commit()

    conn.close()
    return {"success": True, "message": "资料已更新"}

@app.post("/api/user/{token}/keywords")
def user_add_keyword(token: str, payload: KeywordPayload):
    user = _get_user_by_token(token)
    keyword = payload.keyword.strip()
    if not keyword:
        raise HTTPException(status_code=400, detail="关键词不能为空")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO user_keywords (user_id, keyword) VALUES (?, ?)", (user['id'], keyword))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="关键词已存在")
    conn.close()
    return {"success": True, "message": f"已添加关键词: {keyword}"}

@app.delete("/api/user/{token}/keywords/{keyword}")
def user_delete_keyword(token: str, keyword: str):
    user = _get_user_by_token(token)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_keywords WHERE user_id = ? AND keyword = ?", (user['id'], keyword))
    conn.commit()
    conn.close()
    return {"success": True, "message": f"已删除关键词: {keyword}"}

@app.get("/api/user/{token}/papers")
def user_get_papers(token: str, limit: int = 20, offset: int = 0):
    """获取用户关键词匹配的论文历史"""
    user = _get_user_by_token(token)
    keywords = user.get("keywords", [])
    if not keywords:
        return {"papers": [], "total": 0}
    result = get_papers_by_keywords(keywords, limit=min(limit, 100), offset=max(offset, 0))
    return result


@app.post("/api/user/{token}/unsubscribe")
def user_unsubscribe(token: str):
    user = _get_user_by_token(token)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET status='unsubscribed', unsubscribed_at=? WHERE id=?",
        (datetime.now().isoformat(), user['id']),
    )
    conn.commit()
    conn.close()
    return {"success": True, "message": "已取消订阅"}


# ============================================================
# 启动入口
# ============================================================

if __name__ == "__main__":
    import uvicorn

    init_database()

    debug_mode = os.getenv("WEB_DEBUG", os.getenv("FLASK_DEBUG", "False")).lower() == "true"
    port = int(os.getenv("WEB_PORT", os.getenv("FLASK_PORT", "5001")))

    print("=" * 60)
    print("🌐 启动 Web UI 服务器 (FastAPI)...")
    print("=" * 60)
    print(f"📱 访问地址: http://localhost:{port}")
    print(f"🔧 Debug 模式: {'开启' if debug_mode else '关闭'}")
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)

    uvicorn.run("web_ui:app", host="0.0.0.0", port=port, reload=debug_mode)
