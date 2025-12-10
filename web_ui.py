"""
Web UI for Research Agent
提供关键词管理和论文搜索的 Web 界面（基于 FastAPI）
"""
import os
import sqlite3
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
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
    DB_PATH,
)

# 从环境变量读取邮件配置（与 research_agent.py 保持一致）
EMAIL_SENDER = os.environ.get("EMAIL_SENDER", "")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")

app = FastAPI(title="Research Agent Web UI")
templates = Jinja2Templates(directory="templates")
KEYWORDS_FILE = "keywords.txt"


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
        FROM papers
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))
    
    papers = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return papers

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """主页"""
    keywords = load_keywords()
    papers = get_papers_from_db(limit=20)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "keywords": keywords, "papers": papers},
    )


@app.get("/api/keywords")
def get_keywords():
    """获取关键词列表"""
    keywords = load_keywords()
    return {"keywords": keywords}


@app.post("/api/keywords")
def add_keyword(payload: KeywordCreate):
    """添加关键词"""
    keyword = payload.keyword.strip()
    
    if not keyword:
        raise HTTPException(status_code=400, detail="关键词不能为空")
    
    keywords = load_keywords()
    if keyword in keywords:
        raise HTTPException(status_code=400, detail="关键词已存在")
    
    keywords.append(keyword)
    if save_keywords(keywords):
        return {
            "success": True,
            "message": "关键词添加成功",
            "keywords": keywords,
        }
    else:
        raise HTTPException(status_code=500, detail="保存失败")


@app.delete("/api/keywords/{index}")
def delete_keyword(index: int):
    """删除关键词"""
    keywords = load_keywords()
    
    if 0 <= index < len(keywords):
        deleted = keywords.pop(index)
        if save_keywords(keywords):
            return {
                "success": True,
                "message": f"已删除关键词: {deleted}",
                "keywords": keywords,
            }
        else:
            raise HTTPException(status_code=500, detail="保存失败")
    else:
        raise HTTPException(status_code=400, detail="索引无效")


@app.post("/api/search")
def search_papers(payload: SearchRequest):
    """主动搜索论文"""
    keyword = payload.keyword.strip()
    time_range = payload.time_range or "7"  # 默认7天
    max_results = payload.max_results or 10  # 默认10篇
    backup_email = (payload.backup_email or "").strip()  # 备份邮箱
    
    if not keyword:
        raise HTTPException(status_code=400, detail="关键词不能为空")
    
    # 将时间范围字符串转换为天数
    time_range_map = {
        "7": 7,   # 7天
        "30": 30, # 1个月
        "90": 90, # 3个月
        "180": 180, # 6个月
    }

    days = time_range_map.get(time_range, 7)

    # 限制最大结果数量在合理范围内
    max_results = min(max(int(max_results), 1), 100)  # 限制在1-100之间
    
    try:
        # 初始化数据库
        init_database()
        
        # 搜索论文（传入天数参数和最大结果数）
        papers = fetch_papers(keyword, days=days, max_results=max_results)
        
        if not papers:
            time_range_text = {
                "7": "7天",
                "30": "1个月",
                "90": "3个月",
                "180": "6个月",
            }.get(time_range, "7天")
            
            return {
                "success": True,
                "message": f"未找到新论文（关键词: {keyword}, 时间范围: 过去{time_range_text}）",
                "papers": [],
            }
        
        # 为每篇论文生成总结
        results = []
        for paper in papers:
            summary = summarize_paper(paper, keyword)
            save_paper(paper, summary, keyword, sent=False)
            
            results.append({
                'id': paper['id'],
                'title': paper['title'],
                'url': paper['url'],
                'abstract': paper['abstract'],  # 保存完整摘要
                'authors': paper['authors'],
                'date': paper['date'],
                'summary': summary
            })
        
        time_range_text = {
            "7": "7天",
            "30": "1个月",
            "90": "3个月",
            "180": "6个月",
        }.get(time_range, "7天")
        
        # 如果提供了备份邮箱，发送邮件
        email_sent = False
        if backup_email:
            try:
                # 生成邮件HTML内容
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
                    </div>
                    <br>
                    """
                
                # 发送邮件 - 使用统一的send_email函数
                # 临时设置接收邮箱为备份邮箱
                import research_agent

                original_receiver = research_agent.EMAIL_RECEIVER
                research_agent.EMAIL_RECEIVER = backup_email

                try:
                    email_subject = f"论文搜索结果 - {keyword} ({datetime.now().strftime('%Y-%m-%d')})"
                    send_email(report_html, subject=email_subject)
                finally:
                    # 恢复原始接收邮箱
                    research_agent.EMAIL_RECEIVER = original_receiver

                email_sent = True
            except Exception as e:
                print(f"发送备份邮件失败: {e}")
        
        message = f"找到 {len(results)} 篇新论文（时间范围: 过去{time_range_text}, 限制: {max_results} 篇）"
        if email_sent:
            message += f"，已发送到 {backup_email}"

        return {
            "success": True,
            "message": message,
            "papers": results,
            "email_sent": email_sent,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")


@app.post("/api/search_by_author")
def search_papers_by_author(payload: AuthorSearchRequest):
    """
    按作者搜索最近 N 天的论文
    不写入数据库，只返回结果
    """
    author = payload.author.strip()
    days = max(int(payload.days), 1)
    max_results = min(max(int(payload.max_results), 1), 100)

    if not author:
        raise HTTPException(status_code=400, detail="作者姓名不能为空")

    try:
        # 直接调用按作者查询的封装函数，真正按作者字段筛选
        papers = fetch_papers_by_author(author, days=days, max_results=max_results)

        if not papers:
            return {
                "success": True,
                "message": f"未找到作者 {author} 在过去 {days} 天的论文",
                "papers": [],
            }

        results = []
        for paper in papers:
            # 不做 LLM 总结和数据库写入，快速返回结果
            results.append(
                {
                    "id": paper["id"],
                    "title": paper["title"],
                    "url": paper["url"],
                    "abstract": paper["abstract"],
                    "authors": paper["authors"],
                    "date": paper["date"],
                }
            )

        message = f"找到作者 {author} 在过去 {days} 天的 {len(results)} 篇论文（限制: {max_results} 篇）"
        return {
            "success": True,
            "message": message,
            "papers": results,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"作者搜索失败: {str(e)}")


@app.get("/api/papers")
def get_papers(limit: int = 50):
    """获取已保存的论文列表"""
    papers = get_papers_from_db(limit=limit)
    return {"papers": papers}


@app.get("/api/papers/all")
def get_all_papers():
    """获取数据库中的所有论文（不分页）"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, title, url, abstract, authors, date, summary, keyword, sent_at, created_at
        FROM papers
        ORDER BY created_at DESC
    """)
    
    papers = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # 统计信息
    total_count = len(papers)
    keywords_count = {}
    for paper in papers:
        kw = paper.get("keyword", "N/A")
        keywords_count[kw] = keywords_count.get(kw, 0) + 1

    return {
        "papers": papers,
        "total": total_count,
        "keywords_count": keywords_count,
    }


@app.get("/api/papers/{paper_id}")
def get_paper_detail(paper_id: str):
    """获取论文详情"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, title, url, abstract, authors, date, summary, keyword, sent_at, created_at
        FROM papers
        WHERE id = ?
    """, (paper_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {"paper": dict(row)}
    else:
        raise HTTPException(status_code=404, detail="论文不存在")


if __name__ == "__main__":
    import uvicorn

    # 确保数据库已初始化
    init_database()
    
    # 从环境变量读取配置，生产环境默认关闭 debug
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
