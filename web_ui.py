"""
Web UI for Research Agent
提供关键词管理和论文搜索的 Web 界面
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import sqlite3
from datetime import datetime
from research_agent import (
    load_keywords, fetch_papers, summarize_paper, 
    init_database, is_paper_exists, get_cached_summary, save_paper,
    send_email, EMAIL_SENDER, EMAIL_PASSWORD
)
import html as html_escape

app = Flask(__name__)
KEYWORDS_FILE = "keywords.txt"
DB_PATH = "papers.db"

def save_keywords(keywords: list):
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

@app.route('/')
def index():
    """主页"""
    keywords = load_keywords()
    papers = get_papers_from_db(limit=20)
    return render_template('index.html', keywords=keywords, papers=papers)

@app.route('/api/keywords', methods=['GET'])
def get_keywords():
    """获取关键词列表"""
    keywords = load_keywords()
    return jsonify({'keywords': keywords})

@app.route('/api/keywords', methods=['POST'])
def add_keyword():
    """添加关键词"""
    data = request.json
    keyword = data.get('keyword', '').strip()
    
    if not keyword:
        return jsonify({'success': False, 'message': '关键词不能为空'}), 400
    
    keywords = load_keywords()
    if keyword in keywords:
        return jsonify({'success': False, 'message': '关键词已存在'}), 400
    
    keywords.append(keyword)
    if save_keywords(keywords):
        return jsonify({'success': True, 'message': '关键词添加成功', 'keywords': keywords})
    else:
        return jsonify({'success': False, 'message': '保存失败'}), 500

@app.route('/api/keywords/<int:index>', methods=['DELETE'])
def delete_keyword(index):
    """删除关键词"""
    keywords = load_keywords()
    
    if 0 <= index < len(keywords):
        deleted = keywords.pop(index)
        if save_keywords(keywords):
            return jsonify({'success': True, 'message': f'已删除关键词: {deleted}', 'keywords': keywords})
        else:
            return jsonify({'success': False, 'message': '保存失败'}), 500
    else:
        return jsonify({'success': False, 'message': '索引无效'}), 400

@app.route('/api/search', methods=['POST'])
def search_papers():
    """主动搜索论文"""
    data = request.json
    keyword = data.get('keyword', '').strip()
    time_range = data.get('time_range', '7')  # 默认7天
    max_results = data.get('max_results', 10)  # 默认10篇
    backup_email = data.get('backup_email', '').strip()  # 备份邮箱
    
    if not keyword:
        return jsonify({'success': False, 'message': '关键词不能为空'}), 400
    
    # 将时间范围字符串转换为天数
    time_range_map = {
        '7': 7,      # 7天
        '30': 30,    # 1个月
        '90': 90,    # 3个月
        '180': 180   # 6个月
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
                '7': '7天',
                '30': '1个月',
                '90': '3个月',
                '180': '6个月'
            }.get(time_range, '7天')
            
            return jsonify({
                'success': True, 
                'message': f'未找到新论文（关键词: {keyword}, 时间范围: 过去{time_range_text}）',
                'papers': []
            })
        
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
            '7': '7天',
            '30': '1个月',
            '90': '3个月',
            '180': '6个月'
        }.get(time_range, '7天')
        
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
                
                # 发送邮件
                from email.mime.text import MIMEText
                from email.header import Header
                import smtplib
                
                msg = MIMEText(report_html, 'html', 'utf-8')
                msg['From'] = Header("Research Agent", 'utf-8')
                msg['To'] = Header(backup_email, 'utf-8')
                msg['Subject'] = Header(f"论文搜索结果 - {keyword} ({datetime.now().strftime('%Y-%m-%d')})", 'utf-8')
                
                server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.sendmail(EMAIL_SENDER, [backup_email], msg.as_string())
                server.quit()
                
                email_sent = True
            except Exception as e:
                print(f"发送备份邮件失败: {e}")
        
        message = f'找到 {len(results)} 篇新论文（时间范围: 过去{time_range_text}, 限制: {max_results} 篇）'
        if email_sent:
            message += f'，已发送到 {backup_email}'
        
        return jsonify({
            'success': True,
            'message': message,
            'papers': results,
            'email_sent': email_sent
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'搜索失败: {str(e)}'}), 500

@app.route('/api/papers', methods=['GET'])
def get_papers():
    """获取已保存的论文列表"""
    limit = request.args.get('limit', 50, type=int)
    papers = get_papers_from_db(limit=limit)
    return jsonify({'papers': papers})

@app.route('/api/papers/all', methods=['GET'])
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
        kw = paper.get('keyword', 'N/A')
        keywords_count[kw] = keywords_count.get(kw, 0) + 1
    
    return jsonify({
        'papers': papers,
        'total': total_count,
        'keywords_count': keywords_count
    })

@app.route('/api/papers/<paper_id>', methods=['GET'])
def get_paper_detail(paper_id):
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
        return jsonify({'paper': dict(row)})
    else:
        return jsonify({'success': False, 'message': '论文不存在'}), 404

if __name__ == '__main__':
    # 确保数据库已初始化
    init_database()
    
    print("=" * 60)
    print("🌐 启动 Web UI 服务器...")
    print("=" * 60)
    print("📱 访问地址: http://localhost:5001")
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5001)

