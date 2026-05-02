"""web_ui.py API 端点单元测试"""
import os
import sqlite3
import pytest
from unittest.mock import patch, MagicMock

os.environ["APP_ENV"] = "test"
os.environ["DATABASE_PATH"] = "papers.test.db"

from research_agent import DB_PATH


# ============================================================
# Homepage & static pages
# ============================================================

class TestPages:
    def test_index_page(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        assert "Research Agent" in resp.text

    def test_admin_page(self, client):
        resp = client.get("/admin")
        assert resp.status_code == 200

    def test_user_portal_valid(self, client, sample_user):
        resp = client.get(f"/user/{sample_user['token']}")
        assert resp.status_code == 200
        assert "用户设置" in resp.text

    def test_user_portal_invalid_token(self, client):
        resp = client.get("/user/invalid_token_xyz")
        assert resp.status_code == 404


# ============================================================
# Login API
# ============================================================

class TestLoginAPI:
    @patch("web_ui.send_email")
    def test_login_existing_user(self, mock_send, client, sample_user):
        resp = client.post("/api/login", json={"email": "alice@example.com"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        mock_send.assert_called_once()
        # 验证邮件内容包含 portal 链接
        call_args = mock_send.call_args
        assert sample_user["token"] in call_args.kwargs.get("subject", "") or sample_user["token"] in call_args.args[0]

    @patch("web_ui.send_email")
    def test_login_nonexistent_email(self, mock_send, client):
        """不存在的邮箱也应该返回成功（防止枚举）"""
        resp = client.post("/api/login", json={"email": "nobody@example.com"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        mock_send.assert_not_called()

    @patch("web_ui.send_email")
    def test_login_same_response(self, mock_send, client, sample_user):
        """有/无用户返回的 message 格式一致"""
        resp1 = client.post("/api/login", json={"email": "alice@example.com"})
        resp2 = client.post("/api/login", json={"email": "nobody@example.com"})
        assert resp1.json()["message"] == resp2.json()["message"]

    def test_login_invalid_email(self, client):
        resp = client.post("/api/login", json={"email": "not-an-email"})
        assert resp.status_code == 422

    @patch("web_ui.send_email")
    def test_login_pending_user_no_email(self, mock_send, client, pending_user):
        """pending 用户不应发送登录邮件（只有 active 用户才能登录）"""
        resp = client.post("/api/login", json={"email": "pending@example.com"})
        assert resp.status_code == 200
        assert resp.json()["success"] is True
        mock_send.assert_not_called()


# ============================================================
# Subscribe API
# ============================================================

class TestSubscribeAPI:
    @patch("web_ui.send_email")
    def test_subscribe_new_user(self, mock_send, client):
        resp = client.post("/api/subscribe", json={
            "email": "newuser@example.com",
            "name": "New User",
            "lang": "zh",
            "email_frequency": "daily",
            "keywords": ["LLM", "RL"],
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        mock_send.assert_called_once()

        # 验证用户状态是 pending
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM users WHERE email = ?", ("newuser@example.com",))
        row = cursor.fetchone()
        conn.close()
        assert row[0] == "pending"

    @patch("web_ui.send_email")
    def test_subscribe_creates_keywords(self, mock_send, client):
        client.post("/api/subscribe", json={
            "email": "kwuser@example.com",
            "name": "KW User",
            "keywords": ["Deep Learning", "NLP"],
        })
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", ("kwuser@example.com",))
        user_id = cursor.fetchone()["id"]
        cursor.execute("SELECT keyword FROM user_keywords WHERE user_id = ? ORDER BY keyword", (user_id,))
        kws = [r["keyword"] for r in cursor.fetchall()]
        conn.close()
        assert kws == ["Deep Learning", "NLP"]

    def test_subscribe_existing_active_user(self, client, sample_user):
        """已激活用户重复订阅返回 token"""
        resp = client.post("/api/subscribe", json={"email": "alice@example.com"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert data["token"] == sample_user["token"]

    @patch("web_ui.send_email")
    def test_subscribe_reactivate_unsubscribed(self, mock_send, client, sample_user, db_conn):
        # 先退订
        db_conn.cursor().execute("UPDATE users SET status='unsubscribed' WHERE id=?", (sample_user["id"],))
        db_conn.commit()
        # 重新订阅
        resp = client.post("/api/subscribe", json={"email": "alice@example.com"})
        assert resp.status_code == 200
        # 应该是 pending 状态
        cursor = db_conn.cursor()
        cursor.execute("SELECT status FROM users WHERE id=?", (sample_user["id"],))
        assert cursor.fetchone()[0] == "pending"
        mock_send.assert_called_once()

    def test_subscribe_invalid_email(self, client):
        resp = client.post("/api/subscribe", json={"email": "bad-email"})
        assert resp.status_code == 422


# ============================================================
# Verify Email API
# ============================================================

class TestVerifyAPI:
    def test_verify_pending_user(self, client, pending_user):
        resp = client.get(f"/api/verify/{pending_user['token']}")
        assert resp.status_code == 200
        assert "验证成功" in resp.text or "Email Verified" in resp.text

        # 确认状态变为 active
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM users WHERE token = ?", (pending_user["token"],))
        assert cursor.fetchone()[0] == "active"
        conn.close()

    def test_verify_already_active(self, client, sample_user):
        resp = client.get(f"/api/verify/{sample_user['token']}")
        assert resp.status_code == 200
        assert "已验证" in resp.text or "Already Verified" in resp.text

    def test_verify_invalid_token(self, client):
        resp = client.get("/api/verify/invalid_token_xyz")
        assert resp.status_code == 404
        assert "Invalid Link" in resp.text


# ============================================================
# Unsubscribe API
# ============================================================

class TestUnsubscribeAPI:
    def test_unsubscribe_by_email(self, client, sample_user):
        resp = client.post("/api/unsubscribe", json={"email": "alice@example.com"})
        assert resp.status_code == 200
        assert resp.json()["success"] is True

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM users WHERE email = ?", ("alice@example.com",))
        assert cursor.fetchone()[0] == "unsubscribed"
        conn.close()

    def test_unsubscribe_nonexistent(self, client):
        resp = client.post("/api/unsubscribe", json={"email": "nobody@example.com"})
        data = resp.json()
        assert data["success"] is False

    def test_unsubscribe_by_token(self, client, sample_user):
        resp = client.get(f"/api/unsubscribe/{sample_user['token']}")
        assert resp.status_code == 200

    def test_unsubscribe_by_token_invalid(self, client):
        resp = client.get("/api/unsubscribe/invalid_token")
        assert resp.status_code == 404

    def test_user_unsubscribe_endpoint(self, client, sample_user):
        resp = client.post(f"/api/user/{sample_user['token']}/unsubscribe")
        assert resp.status_code == 200
        assert resp.json()["success"] is True


# ============================================================
# User Profile API
# ============================================================

class TestUserProfileAPI:
    def test_get_profile(self, client, sample_user):
        resp = client.get(f"/api/user/{sample_user['token']}/profile")
        assert resp.status_code == 200
        data = resp.json()
        user = data["user"]
        assert user["email"] == "alice@example.com"
        assert user["name"] == "Alice"
        assert "keywords" in user

    def test_get_profile_invalid_token(self, client):
        resp = client.get("/api/user/invalid_token/profile")
        assert resp.status_code == 404

    def test_update_profile(self, client, sample_user):
        resp = client.put(
            f"/api/user/{sample_user['token']}/profile",
            json={"name": "Alice Updated", "lang": "en", "email_frequency": "weekly"},
        )
        assert resp.status_code == 200
        assert resp.json()["success"] is True

        # 验证更新
        resp2 = client.get(f"/api/user/{sample_user['token']}/profile")
        user = resp2.json()["user"]
        assert user["name"] == "Alice Updated"
        assert user["lang"] == "en"
        assert user["email_frequency"] == "weekly"

    def test_update_profile_partial(self, client, sample_user):
        """只更新部分字段"""
        resp = client.put(
            f"/api/user/{sample_user['token']}/profile",
            json={"name": "New Name"},
        )
        assert resp.status_code == 200
        user = client.get(f"/api/user/{sample_user['token']}/profile").json()["user"]
        assert user["name"] == "New Name"
        assert user["lang"] == "zh"  # 未变


# ============================================================
# User Keywords API
# ============================================================

class TestUserKeywordsAPI:
    def test_add_keyword(self, client, sample_user):
        resp = client.post(
            f"/api/user/{sample_user['token']}/keywords",
            json={"keyword": "Transformer"},
        )
        assert resp.status_code == 200
        assert resp.json()["success"] is True

        # 验证
        profile = client.get(f"/api/user/{sample_user['token']}/profile").json()["user"]
        assert "Transformer" in profile["keywords"]

    def test_add_duplicate_keyword(self, client, sample_user_with_keywords):
        resp = client.post(
            f"/api/user/{sample_user_with_keywords['token']}/keywords",
            json={"keyword": "LLM"},
        )
        assert resp.status_code == 400

    def test_add_empty_keyword(self, client, sample_user):
        resp = client.post(
            f"/api/user/{sample_user['token']}/keywords",
            json={"keyword": "  "},
        )
        assert resp.status_code == 400

    def test_delete_keyword(self, client, sample_user_with_keywords):
        resp = client.delete(f"/api/user/{sample_user_with_keywords['token']}/keywords/LLM")
        assert resp.status_code == 200

        profile = client.get(f"/api/user/{sample_user_with_keywords['token']}/profile").json()["user"]
        assert "LLM" not in profile["keywords"]
        assert "Reinforcement Learning" in profile["keywords"]


# ============================================================
# User Papers API
# ============================================================

class TestUserPapersAPI:
    def test_get_papers(self, client, sample_user_with_keywords, sample_papers):
        resp = client.get(f"/api/user/{sample_user_with_keywords['token']}/papers")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 4  # 2 LLM + 2 RL
        assert len(data["papers"]) == 4

    def test_get_papers_pagination(self, client, sample_user_with_keywords, sample_papers):
        resp = client.get(f"/api/user/{sample_user_with_keywords['token']}/papers?limit=2&offset=0")
        data = resp.json()
        assert data["total"] == 4
        assert len(data["papers"]) == 2

        resp2 = client.get(f"/api/user/{sample_user_with_keywords['token']}/papers?limit=2&offset=2")
        data2 = resp2.json()
        assert len(data2["papers"]) == 2

        # 两页的论文不重复
        ids_page1 = {p["id"] for p in data["papers"]}
        ids_page2 = {p["id"] for p in data2["papers"]}
        assert ids_page1.isdisjoint(ids_page2)

    def test_get_papers_no_keywords(self, client, sample_user, sample_papers):
        """没有关键词的用户返回空"""
        resp = client.get(f"/api/user/{sample_user['token']}/papers")
        data = resp.json()
        assert data["total"] == 0
        assert data["papers"] == []

    def test_get_papers_invalid_token(self, client):
        resp = client.get("/api/user/invalid_token/papers")
        assert resp.status_code == 404

    def test_get_papers_limit_cap(self, client, sample_user_with_keywords, sample_papers):
        """limit 上限为 100"""
        resp = client.get(f"/api/user/{sample_user_with_keywords['token']}/papers?limit=999")
        assert resp.status_code == 200


# ============================================================
# Global Keywords API
# ============================================================

class TestGlobalKeywordsAPI:
    def test_get_keywords(self, client):
        resp = client.get("/api/keywords")
        assert resp.status_code == 200
        assert "keywords" in resp.json()

    def test_add_and_delete_keyword(self, client, monkeypatch, tmp_path):
        kw_file = tmp_path / "keywords.txt"
        kw_file.write_text("")
        monkeypatch.setattr("web_ui.KEYWORDS_FILE", str(kw_file))
        monkeypatch.setattr("research_agent.KEYWORDS_FILE", str(kw_file))

        # Add
        resp = client.post("/api/keywords", json={"keyword": "TestKW"})
        assert resp.status_code == 200
        assert resp.json()["success"] is True

        # Verify
        resp2 = client.get("/api/keywords")
        assert "TestKW" in resp2.json()["keywords"]

        # Delete (index 0)
        resp3 = client.delete("/api/keywords/0")
        assert resp3.status_code == 200

    def test_add_empty_keyword(self, client):
        resp = client.post("/api/keywords", json={"keyword": "  "})
        assert resp.status_code == 400


# ============================================================
# Papers API (global)
# ============================================================

class TestPapersAPI:
    def test_get_papers(self, client, sample_papers):
        resp = client.get("/api/papers?limit=3")
        assert resp.status_code == 200
        assert len(resp.json()["papers"]) == 3

    def test_get_all_papers(self, client, sample_papers):
        resp = client.get("/api/papers/all")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 5
        assert "keywords_count" in data

    def test_get_paper_detail(self, client, sample_papers):
        resp = client.get("/api/papers/paper1")
        assert resp.status_code == 200
        assert resp.json()["paper"]["title"] == "LLM Reasoning Survey"

    def test_get_paper_detail_not_found(self, client):
        resp = client.get("/api/papers/nonexistent")
        assert resp.status_code == 404

    def test_export_csv(self, client, sample_papers):
        resp = client.get("/api/papers/export/csv")
        assert resp.status_code == 200
        assert "text/csv" in resp.headers["content-type"]
        assert "paper1" in resp.text


# ============================================================
# Admin Login API
# ============================================================

class TestAdminLoginAPI:
    def test_admin_login_success(self, client):
        from web_ui import ADMIN_PASSWORD
        resp = client.post("/api/admin/login", json={"password": ADMIN_PASSWORD})
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert "token" in data
        # 验证 cookie 被设置
        assert "admin_token" in resp.cookies

    def test_admin_login_wrong_password(self, client):
        resp = client.post("/api/admin/login", json={"password": "wrong_password"})
        assert resp.status_code == 401

    def test_admin_unauthorized_without_login(self, client):
        resp = client.get("/api/admin/dashboard")
        assert resp.status_code == 401


# ============================================================
# Admin Dashboard API
# ============================================================

class TestAdminDashboardAPI:
    def test_dashboard(self, admin_client, sample_user, sample_papers):
        resp = admin_client.get("/api/admin/dashboard")
        assert resp.status_code == 200
        data = resp.json()
        assert data["active_users"] == 1
        assert data["total_users"] == 1
        assert data["total_papers"] == 5

    def test_dashboard_empty(self, admin_client):
        resp = admin_client.get("/api/admin/dashboard")
        assert resp.status_code == 200
        data = resp.json()
        assert data["active_users"] == 0
        assert data["total_papers"] == 0


# ============================================================
# Admin Users API
# ============================================================

class TestAdminUsersAPI:
    def test_list_users(self, admin_client, sample_user):
        resp = admin_client.get("/api/admin/users")
        assert resp.status_code == 200
        users = resp.json()["users"]
        assert len(users) == 1
        assert users[0]["email"] == "alice@example.com"

    def test_list_users_with_keywords(self, admin_client, sample_user_with_keywords):
        resp = admin_client.get("/api/admin/users")
        users = resp.json()["users"]
        assert len(users[0]["keywords"]) == 2

    def test_get_user(self, admin_client, sample_user):
        resp = admin_client.get(f"/api/admin/users/{sample_user['id']}")
        assert resp.status_code == 200
        assert resp.json()["user"]["email"] == "alice@example.com"

    def test_get_user_not_found(self, admin_client):
        resp = admin_client.get("/api/admin/users/99999")
        assert resp.status_code == 404

    def test_update_user_name(self, admin_client, sample_user):
        resp = admin_client.put(
            f"/api/admin/users/{sample_user['id']}",
            json={"name": "Alice Admin Updated"},
        )
        assert resp.status_code == 200
        user = admin_client.get(f"/api/admin/users/{sample_user['id']}").json()["user"]
        assert user["name"] == "Alice Admin Updated"

    def test_update_user_status_unsubscribed(self, admin_client, sample_user):
        resp = admin_client.put(
            f"/api/admin/users/{sample_user['id']}",
            json={"status": "unsubscribed"},
        )
        assert resp.status_code == 200
        user = admin_client.get(f"/api/admin/users/{sample_user['id']}").json()["user"]
        assert user["status"] == "unsubscribed"
        assert user["unsubscribed_at"] is not None

    def test_update_user_status_reactivate(self, admin_client, sample_user, db_conn):
        db_conn.cursor().execute("UPDATE users SET status='unsubscribed', unsubscribed_at='2026-01-01' WHERE id=?", (sample_user["id"],))
        db_conn.commit()
        resp = admin_client.put(
            f"/api/admin/users/{sample_user['id']}",
            json={"status": "active"},
        )
        assert resp.status_code == 200
        user = admin_client.get(f"/api/admin/users/{sample_user['id']}").json()["user"]
        assert user["status"] == "active"
        assert user["unsubscribed_at"] is None

    def test_update_user_no_changes(self, admin_client, sample_user):
        resp = admin_client.put(
            f"/api/admin/users/{sample_user['id']}",
            json={},
        )
        assert resp.status_code == 200
        assert resp.json()["message"] == "无更新"

    def test_delete_user(self, admin_client, sample_user_with_keywords):
        uid = sample_user_with_keywords["id"]
        resp = admin_client.delete(f"/api/admin/users/{uid}")
        assert resp.status_code == 200
        # 验证用户和关键词都被删除
        resp2 = admin_client.get(f"/api/admin/users/{uid}")
        assert resp2.status_code == 404
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM user_keywords WHERE user_id = ?", (uid,))
        assert cursor.fetchone()[0] == 0
        conn.close()


# ============================================================
# Admin Keywords API
# ============================================================

class TestAdminKeywordsAPI:
    def test_add_keyword(self, admin_client, sample_user):
        resp = admin_client.post(
            f"/api/admin/users/{sample_user['id']}/keywords",
            json={"keyword": "NewKW"},
        )
        assert resp.status_code == 200
        user = admin_client.get(f"/api/admin/users/{sample_user['id']}").json()["user"]
        assert "NewKW" in user["keywords"]

    def test_add_duplicate_keyword(self, admin_client, sample_user_with_keywords):
        resp = admin_client.post(
            f"/api/admin/users/{sample_user_with_keywords['id']}/keywords",
            json={"keyword": "LLM"},
        )
        assert resp.status_code == 400

    def test_add_empty_keyword(self, admin_client, sample_user):
        resp = admin_client.post(
            f"/api/admin/users/{sample_user['id']}/keywords",
            json={"keyword": "  "},
        )
        assert resp.status_code == 400

    def test_delete_keyword(self, admin_client, sample_user_with_keywords):
        resp = admin_client.delete(
            f"/api/admin/users/{sample_user_with_keywords['id']}/keywords/LLM"
        )
        assert resp.status_code == 200
        user = admin_client.get(f"/api/admin/users/{sample_user_with_keywords['id']}").json()["user"]
        assert "LLM" not in user["keywords"]


# ============================================================
# Admin Papers API
# ============================================================

class TestAdminPapersAPI:
    def test_list_papers(self, admin_client, sample_papers):
        resp = admin_client.get("/api/admin/papers")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 5
        assert "keywords_count" in data

    def test_delete_paper(self, admin_client, sample_papers):
        resp = admin_client.delete("/api/admin/papers/paper1")
        assert resp.status_code == 200
        # 确认已删除
        resp2 = admin_client.get("/api/admin/papers")
        ids = [p["id"] for p in resp2.json()["papers"]]
        assert "paper1" not in ids

    def test_delete_paper_not_found(self, admin_client):
        resp = admin_client.delete("/api/admin/papers/nonexistent")
        assert resp.status_code == 404


# ============================================================
# Search API (mock arXiv + OpenAI)
# ============================================================

class TestSearchAPI:
    @patch("web_ui.summarize_paper")
    @patch("web_ui.fetch_papers")
    def test_search_papers(self, mock_fetch, mock_summarize, client):
        mock_fetch.return_value = [
            {"id": "s1", "title": "Search Result", "url": "http://arxiv.org/s1",
             "abstract": "Abstract", "authors": "Author", "date": "2026-03-20"},
        ]
        mock_summarize.return_value = "Mocked summary"

        resp = client.post("/api/search", json={"keyword": "LLM", "time_range": "7", "max_results": 5})
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert len(data["papers"]) == 1
        assert data["papers"][0]["summary"] == "Mocked summary"
        mock_fetch.assert_called_once()
        mock_summarize.assert_called_once()

    @patch("web_ui.fetch_papers")
    def test_search_no_results(self, mock_fetch, client):
        mock_fetch.return_value = []
        resp = client.post("/api/search", json={"keyword": "nothing"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert data["papers"] == []

    def test_search_empty_keyword(self, client):
        resp = client.post("/api/search", json={"keyword": ""})
        assert resp.status_code == 400

    @patch("web_ui.send_email")
    @patch("web_ui.summarize_paper")
    @patch("web_ui.fetch_papers")
    def test_search_with_email_backup(self, mock_fetch, mock_summarize, mock_email, client):
        mock_fetch.return_value = [
            {"id": "e1", "title": "Email Paper", "url": "http://arxiv.org/e1",
             "abstract": "Abstract", "authors": "Author", "date": "2026-03-20"},
        ]
        mock_summarize.return_value = "Summary"

        resp = client.post("/api/search", json={
            "keyword": "LLM", "backup_email": "backup@example.com",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["email_sent"] is True
        mock_email.assert_called_once()

    @patch("web_ui.fetch_papers")
    def test_search_api_error(self, mock_fetch, client):
        mock_fetch.side_effect = Exception("arXiv down")
        resp = client.post("/api/search", json={"keyword": "LLM"})
        assert resp.status_code == 500


# ============================================================
# Author Search API
# ============================================================

class TestAuthorSearchAPI:
    @patch("web_ui.fetch_papers_by_author")
    def test_search_by_author(self, mock_fetch, client):
        mock_fetch.return_value = [
            {"id": "a1", "title": "Author Paper", "url": "http://arxiv.org/a1",
             "abstract": "Abstract", "authors": "Yann LeCun", "date": "2026-03-20"},
        ]
        resp = client.post("/api/search_by_author", json={"author": "Yann LeCun", "days": 30, "max_results": 10})
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert len(data["papers"]) == 1

    @patch("web_ui.fetch_papers_by_author")
    def test_author_search_no_results(self, mock_fetch, client):
        mock_fetch.return_value = []
        resp = client.post("/api/search_by_author", json={"author": "Nobody"})
        assert resp.status_code == 200
        assert resp.json()["papers"] == []

    def test_author_search_empty_name(self, client):
        resp = client.post("/api/search_by_author", json={"author": ""})
        assert resp.status_code == 400

    @patch("web_ui.fetch_papers_by_author")
    def test_author_search_error(self, mock_fetch, client):
        mock_fetch.side_effect = Exception("API error")
        resp = client.post("/api/search_by_author", json={"author": "Test"})
        assert resp.status_code == 500
