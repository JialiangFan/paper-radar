"""Shared fixtures for pytest."""
import os
import sqlite3
import secrets
import pytest

# Force test environment before importing application modules
os.environ["APP_ENV"] = "test"
os.environ["DATABASE_PATH"] = "papers.test.db"
os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("EMAIL_SENDER", "test@example.com")

from research_agent import init_database, DB_PATH


@pytest.fixture(autouse=True)
def clean_test_db():
    """每个测试前重置测试数据库"""
    # 删除旧的测试数据库
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    # 初始化全新数据库
    init_database()
    yield
    # 测试后清理
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)


@pytest.fixture
def db_conn():
    """返回一个数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


@pytest.fixture
def sample_user(db_conn):
    """创建一个测试用户并返回其信息"""
    token = secrets.token_urlsafe(32)
    cursor = db_conn.cursor()
    cursor.execute(
        "INSERT INTO users (email, name, lang, status, token, email_frequency) VALUES (?, ?, ?, ?, ?, ?)",
        ("alice@example.com", "Alice", "zh", "active", token, "daily"),
    )
    db_conn.commit()
    user_id = cursor.lastrowid
    return {"id": user_id, "email": "alice@example.com", "name": "Alice", "token": token}


@pytest.fixture
def pending_user(db_conn):
    """创建一个待验证用户"""
    token = secrets.token_urlsafe(32)
    cursor = db_conn.cursor()
    cursor.execute(
        "INSERT INTO users (email, name, lang, status, token, email_frequency) VALUES (?, ?, ?, ?, ?, ?)",
        ("pending@example.com", "Pending", "en", "pending", token, "daily"),
    )
    db_conn.commit()
    user_id = cursor.lastrowid
    return {"id": user_id, "email": "pending@example.com", "token": token}


@pytest.fixture
def sample_user_with_keywords(sample_user, db_conn):
    """创建带关键词的测试用户"""
    cursor = db_conn.cursor()
    for kw in ["LLM", "Reinforcement Learning"]:
        cursor.execute(
            "INSERT INTO user_keywords (user_id, keyword) VALUES (?, ?)",
            (sample_user["id"], kw),
        )
    db_conn.commit()
    sample_user["keywords"] = ["LLM", "Reinforcement Learning"]
    return sample_user


@pytest.fixture
def sample_papers(db_conn):
    """插入测试论文数据"""
    cursor = db_conn.cursor()
    papers = [
        ("paper1", "LLM Reasoning Survey", "http://arxiv.org/1", "Abstract about LLM", "Author A", "2026-03-20", "Summary of LLM paper", "LLM"),
        ("paper2", "RL for Robotics", "http://arxiv.org/2", "Abstract about RL", "Author B", "2026-03-19", "Summary of RL paper", "Reinforcement Learning"),
        ("paper3", "Diffusion Models", "http://arxiv.org/3", "Abstract about diffusion", "Author C", "2026-03-18", "Summary of diffusion paper", "Diffusion"),
        ("paper4", "LLM Alignment", "http://arxiv.org/4", "Abstract about alignment", "Author D", "2026-03-17", "Summary of alignment", "LLM"),
        ("paper5", "Deep RL Advances", "http://arxiv.org/5", "Abstract about deep RL", "Author E", "2026-03-16", "Summary of deep RL", "Reinforcement Learning"),
    ]
    for p in papers:
        cursor.execute(
            "INSERT INTO papers (id, title, url, abstract, authors, date, summary, keyword) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            p,
        )
    db_conn.commit()
    return papers


@pytest.fixture
def sample_user_with_keywords_and_papers(sample_user_with_keywords, db_conn):
    """创建带关键词和匹配论文的用户"""
    cursor = db_conn.cursor()
    papers = [
        ("p1", "LLM Paper", "http://arxiv.org/p1", "Abstract", "Author A", "2026-03-20", "Summary", "LLM"),
        ("p2", "RL Paper", "http://arxiv.org/p2", "Abstract", "Author B", "2026-03-19", "Summary", "Reinforcement Learning"),
    ]
    for p in papers:
        cursor.execute(
            "INSERT INTO papers (id, title, url, abstract, authors, date, summary, keyword) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", p
        )
    db_conn.commit()
    return sample_user_with_keywords


@pytest.fixture
def client():
    """FastAPI TestClient"""
    from starlette.testclient import TestClient
    from web_ui import app

    with TestClient(app) as c:
        yield c


@pytest.fixture
def admin_client(client):
    """已登录的管理员 TestClient"""
    from web_ui import ADMIN_PASSWORD
    resp = client.post("/api/admin/login", json={"password": ADMIN_PASSWORD})
    assert resp.status_code == 200
    return client
