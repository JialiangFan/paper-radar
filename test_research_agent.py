"""research_agent.py 单元测试"""
import os
import sqlite3
import pytest

os.environ["APP_ENV"] = "test"
os.environ["DATABASE_PATH"] = "papers.test.db"

from research_agent import (
    init_database,
    save_paper,
    is_paper_exists,
    get_cached_summary,
    get_active_users,
    get_user_keywords,
    get_papers_by_keywords,
    get_recent_papers_from_db,
    should_send_to_user,
    update_user_last_sent,
    load_keywords,
    DB_PATH,
)
from datetime import datetime, timedelta


# ============================================================
# Database initialization
# ============================================================

class TestInitDatabase:
    def test_creates_tables(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}
        conn.close()
        assert "papers" in tables
        assert "users" in tables
        assert "user_keywords" in tables

    def test_creates_indexes(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indexes = {row[0] for row in cursor.fetchall()}
        conn.close()
        assert "idx_paper_keyword" in indexes
        assert "idx_paper_date" in indexes
        assert "idx_user_email" in indexes
        assert "idx_user_token" in indexes

    def test_idempotent(self):
        """多次调用 init_database 不应报错"""
        init_database()
        init_database()


# ============================================================
# Paper CRUD
# ============================================================

class TestPaperCrud:
    def test_save_and_exists(self):
        paper = {
            "id": "test_paper_1",
            "title": "Test Paper",
            "url": "http://example.com",
            "abstract": "Test abstract",
            "authors": "Test Author",
            "date": "2026-01-01",
        }
        assert not is_paper_exists("test_paper_1")
        save_paper(paper, "Test summary", "TestKW", sent=False)
        assert is_paper_exists("test_paper_1")

    def test_get_cached_summary(self):
        paper = {
            "id": "cache_test",
            "title": "Cache Test",
            "url": "http://example.com",
            "abstract": "Abstract",
            "authors": "Author",
            "date": "2026-01-01",
        }
        assert get_cached_summary("cache_test") is None
        save_paper(paper, "Cached summary", "KW")
        assert get_cached_summary("cache_test") == "Cached summary"

    def test_save_paper_sent_flag(self):
        paper = {
            "id": "sent_test",
            "title": "Sent Test",
            "url": "http://example.com",
            "abstract": "Abstract",
            "authors": "Author",
            "date": "2026-01-01",
        }
        save_paper(paper, "Summary", "KW", sent=True)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT sent_at FROM papers WHERE id = ?", ("sent_test",))
        row = cursor.fetchone()
        conn.close()
        assert row[0] is not None

    def test_save_paper_not_sent(self):
        paper = {
            "id": "not_sent",
            "title": "Not Sent",
            "url": "http://example.com",
            "abstract": "Abstract",
            "authors": "Author",
            "date": "2026-01-01",
        }
        save_paper(paper, "Summary", "KW", sent=False)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT sent_at FROM papers WHERE id = ?", ("not_sent",))
        row = cursor.fetchone()
        conn.close()
        assert row[0] is None


# ============================================================
# User helpers
# ============================================================

class TestUserHelpers:
    def test_get_active_users(self, sample_user):
        users = get_active_users()
        assert len(users) == 1
        assert users[0]["email"] == "alice@example.com"

    def test_get_active_users_excludes_pending(self, pending_user):
        users = get_active_users()
        assert len(users) == 0

    def test_get_user_keywords(self, sample_user_with_keywords):
        kws = get_user_keywords(sample_user_with_keywords["id"])
        assert set(kws) == {"LLM", "Reinforcement Learning"}

    def test_get_user_keywords_empty(self, sample_user):
        kws = get_user_keywords(sample_user["id"])
        assert kws == []

    def test_update_user_last_sent(self, sample_user):
        update_user_last_sent(sample_user["id"])
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT last_sent_at FROM users WHERE id = ?", (sample_user["id"],))
        row = cursor.fetchone()
        conn.close()
        assert row[0] is not None


# ============================================================
# should_send_to_user
# ============================================================

class TestShouldSendToUser:
    def test_never_sent(self, sample_user):
        assert should_send_to_user(sample_user, datetime.now()) is True

    def test_daily_too_soon(self):
        user = {"email_frequency": "daily", "last_sent_at": datetime.now().isoformat()}
        assert should_send_to_user(user, datetime.now()) is False

    def test_daily_ready(self):
        user = {"email_frequency": "daily", "last_sent_at": (datetime.now() - timedelta(hours=21)).isoformat()}
        assert should_send_to_user(user, datetime.now()) is True

    def test_weekly_too_soon(self):
        user = {"email_frequency": "weekly", "last_sent_at": (datetime.now() - timedelta(days=3)).isoformat()}
        assert should_send_to_user(user, datetime.now()) is False

    def test_weekly_ready(self):
        user = {"email_frequency": "weekly", "last_sent_at": (datetime.now() - timedelta(days=8)).isoformat()}
        assert should_send_to_user(user, datetime.now()) is True

    def test_every_3_days_ready(self):
        user = {"email_frequency": "every_3_days", "last_sent_at": (datetime.now() - timedelta(days=4)).isoformat()}
        assert should_send_to_user(user, datetime.now()) is True


# ============================================================
# get_papers_by_keywords
# ============================================================

class TestGetPapersByKeywords:
    def test_basic_query(self, sample_papers):
        result = get_papers_by_keywords(["LLM"])
        assert result["total"] == 2
        assert len(result["papers"]) == 2
        assert all(p["keyword"] == "LLM" for p in result["papers"])

    def test_multiple_keywords(self, sample_papers):
        result = get_papers_by_keywords(["LLM", "Reinforcement Learning"])
        assert result["total"] == 4
        assert len(result["papers"]) == 4

    def test_pagination_limit(self, sample_papers):
        result = get_papers_by_keywords(["LLM", "Reinforcement Learning"], limit=2, offset=0)
        assert result["total"] == 4
        assert len(result["papers"]) == 2

    def test_pagination_offset(self, sample_papers):
        result = get_papers_by_keywords(["LLM", "Reinforcement Learning"], limit=2, offset=2)
        assert result["total"] == 4
        assert len(result["papers"]) == 2

    def test_no_match(self, sample_papers):
        result = get_papers_by_keywords(["NonExistentKeyword"])
        assert result["total"] == 0
        assert result["papers"] == []

    def test_empty_keywords(self):
        result = get_papers_by_keywords([])
        assert result["total"] == 0
        assert result["papers"] == []

    def test_order_by_created_at_desc(self, sample_papers):
        result = get_papers_by_keywords(["LLM"])
        # Both paper1 and paper4 have keyword LLM
        ids = [p["id"] for p in result["papers"]]
        assert set(ids) == {"paper1", "paper4"}


# ============================================================
# get_recent_papers_from_db
# ============================================================

class TestGetRecentPapers:
    def test_returns_sent_papers(self):
        paper = {
            "id": "recent1",
            "title": "Recent Paper",
            "url": "http://example.com",
            "abstract": "Abstract",
            "authors": "Author",
            "date": datetime.now().strftime("%Y-%m-%d"),
        }
        save_paper(paper, "Summary", "KW", sent=True)
        results = get_recent_papers_from_db(days=7, limit=10)
        assert len(results) == 1
        assert results[0]["id"] == "recent1"

    def test_excludes_unsent(self):
        paper = {
            "id": "unsent1",
            "title": "Unsent Paper",
            "url": "http://example.com",
            "abstract": "Abstract",
            "authors": "Author",
            "date": datetime.now().strftime("%Y-%m-%d"),
        }
        save_paper(paper, "Summary", "KW", sent=False)
        results = get_recent_papers_from_db(days=7, limit=10)
        assert len(results) == 0


# ============================================================
# load_keywords
# ============================================================

class TestLoadKeywords:
    def test_loads_from_file(self, tmp_path, monkeypatch):
        kw_file = tmp_path / "keywords.txt"
        kw_file.write_text("keyword1\nkeyword2\n# comment\n\n")
        monkeypatch.setattr("research_agent.KEYWORDS_FILE", str(kw_file))
        result = load_keywords()
        assert result == ["keyword1", "keyword2"]

    def test_default_when_missing(self, monkeypatch):
        monkeypatch.setattr("research_agent.KEYWORDS_FILE", "/nonexistent/keywords.txt")
        result = load_keywords()
        assert len(result) > 0  # 返回默认关键词
