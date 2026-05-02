"""邮件发送函数单元测试"""
import os
import pytest
from unittest.mock import patch, MagicMock

os.environ["APP_ENV"] = "test"
os.environ["DATABASE_PATH"] = "papers.test.db"

from research_agent import (
    send_email,
    send_email_via_smtp,
    send_email_via_mailgun,
    _build_paper_html,
)


# ============================================================
# send_email routing
# ============================================================

class TestSendEmailRouting:
    @patch("research_agent.USE_MAILGUN_API", False)
    @patch("research_agent.send_email_via_smtp")
    def test_default_uses_smtp(self, mock_smtp):
        mock_smtp.return_value = True
        result = send_email("<p>Hello</p>", subject="Test", to="user@example.com")
        assert result is True
        mock_smtp.assert_called_once_with("<p>Hello</p>", "Test", to="user@example.com")

    @patch("research_agent.send_email_via_mailgun")
    @patch("research_agent.USE_MAILGUN_API", True)
    @patch("research_agent.MAILGUN_API_KEY", "test-key")
    @patch("research_agent.MAILGUN_DOMAIN", "mg.example.com")
    def test_mailgun_when_configured(self, mock_mailgun):
        mock_mailgun.return_value = True
        result = send_email("<p>Hello</p>", subject="Test", to="user@example.com")
        assert result is True
        mock_mailgun.assert_called_once()

    @patch("research_agent.send_email_via_smtp")
    @patch("research_agent.send_email_via_mailgun")
    @patch("research_agent.USE_MAILGUN_API", True)
    @patch("research_agent.MAILGUN_API_KEY", "test-key")
    @patch("research_agent.MAILGUN_DOMAIN", "mg.example.com")
    def test_fallback_to_smtp_on_mailgun_failure(self, mock_mailgun, mock_smtp):
        mock_mailgun.side_effect = Exception("Mailgun error")
        mock_smtp.return_value = True
        result = send_email("<p>Hello</p>", subject="Test", to="user@example.com")
        assert result is True
        mock_mailgun.assert_called_once()
        mock_smtp.assert_called_once()

    @patch("research_agent.USE_MAILGUN_API", False)
    @patch("research_agent.send_email_via_smtp")
    def test_default_subject(self, mock_smtp):
        mock_smtp.return_value = True
        send_email("<p>Hello</p>", to="user@example.com")
        call_args = mock_smtp.call_args
        assert "今日论文日报" in call_args.args[1]


# ============================================================
# send_email_via_smtp
# ============================================================

class TestSendEmailViaSMTP:
    @patch("research_agent.smtplib.SMTP")
    def test_smtp_send(self, mock_smtp_cls):
        mock_server = MagicMock()
        mock_smtp_cls.return_value = mock_server

        result = send_email_via_smtp("<p>Test</p>", "Subject", to="user@example.com")
        assert result is True
        mock_server.starttls.assert_called_once()
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()

    @patch("research_agent.SMTP_USE_SSL", True)
    @patch("research_agent.smtplib.SMTP_SSL")
    def test_smtp_ssl(self, mock_smtp_ssl_cls):
        mock_server = MagicMock()
        mock_smtp_ssl_cls.return_value = mock_server

        result = send_email_via_smtp("<p>Test</p>", "Subject", to="user@example.com")
        assert result is True
        mock_smtp_ssl_cls.assert_called_once()
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()

    @patch("research_agent.EMAIL_PASSWORD", "secret")
    @patch("research_agent.smtplib.SMTP")
    def test_smtp_with_login(self, mock_smtp_cls):
        mock_server = MagicMock()
        mock_smtp_cls.return_value = mock_server

        send_email_via_smtp("<p>Test</p>", "Subject", to="user@example.com")
        mock_server.login.assert_called_once()

    @patch("research_agent.EMAIL_PASSWORD", "")
    @patch("research_agent.smtplib.SMTP")
    def test_smtp_without_login(self, mock_smtp_cls):
        mock_server = MagicMock()
        mock_smtp_cls.return_value = mock_server

        send_email_via_smtp("<p>Test</p>", "Subject", to="user@example.com")
        mock_server.login.assert_not_called()


# ============================================================
# send_email_via_mailgun
# ============================================================

class TestSendEmailViaMailgun:
    @patch("research_agent.MAILGUN_API_KEY", "test-key")
    @patch("research_agent.MAILGUN_DOMAIN", "mg.example.com")
    @patch("research_agent.requests.post")
    def test_mailgun_success(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"id": "msg-123"}
        mock_post.return_value = mock_resp

        result = send_email_via_mailgun("<p>Test</p>", "Subject", to="user@example.com")
        assert result is True
        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args
        assert call_kwargs.kwargs["auth"] == ("api", "test-key")

    @patch("research_agent.MAILGUN_API_KEY", "test-key")
    @patch("research_agent.MAILGUN_DOMAIN", "mg.example.com")
    @patch("research_agent.requests.post")
    def test_mailgun_failure(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 400
        mock_resp.text = "Bad request"
        mock_post.return_value = mock_resp

        with pytest.raises(Exception, match="Mailgun API错误"):
            send_email_via_mailgun("<p>Test</p>", "Subject", to="user@example.com")

    @patch("research_agent.MAILGUN_API_KEY", "")
    def test_mailgun_missing_api_key(self):
        with pytest.raises(ValueError, match="MAILGUN_API_KEY"):
            send_email_via_mailgun("<p>Test</p>", "Subject", to="user@example.com")

    @patch("research_agent.MAILGUN_API_KEY", "key")
    @patch("research_agent.MAILGUN_DOMAIN", "")
    def test_mailgun_missing_domain(self):
        with pytest.raises(ValueError, match="MAILGUN_DOMAIN"):
            send_email_via_mailgun("<p>Test</p>", "Subject", to="user@example.com")


# ============================================================
# _build_paper_html
# ============================================================

class TestBuildPaperHtml:
    def test_basic_html(self):
        paper = {
            "title": "Test Paper <script>",
            "url": "http://example.com",
            "authors": "Author A & Author B",
            "date": "2026-01-01",
        }
        html = _build_paper_html(paper, "Summary with <b>tags</b>")
        assert "Test Paper &lt;script&gt;" in html
        assert "Author A &amp; Author B" in html
        assert "http://example.com" in html
        assert "Summary with &lt;b&gt;tags&lt;/b&gt;" in html

    def test_empty_summary(self):
        paper = {"title": "T", "url": "http://x.com", "authors": "", "date": ""}
        html = _build_paper_html(paper, "")
        assert "<h3>" in html

    def test_none_summary(self):
        paper = {"title": "T", "url": "http://x.com", "authors": "", "date": ""}
        html = _build_paper_html(paper, None)
        assert "<h3>" in html


# ============================================================
# summarize_paper (mock OpenAI)
# ============================================================

class TestSummarizePaper:
    @patch("research_agent.client")
    def test_summarize_calls_api(self, mock_openai_client):
        from research_agent import summarize_paper
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Generated summary"
        mock_openai_client.chat.completions.create.return_value = mock_response

        paper = {
            "id": "sum_test_1",
            "title": "Test",
            "url": "http://x.com",
            "abstract": "Abstract",
            "authors": "Author",
            "date": "2026-01-01",
        }
        result = summarize_paper(paper, "KW")
        assert result == "Generated summary"
        mock_openai_client.chat.completions.create.assert_called_once()

    @patch("research_agent.client")
    def test_summarize_uses_cache(self, mock_openai_client):
        from research_agent import summarize_paper, save_paper
        paper = {
            "id": "cached_sum",
            "title": "Cached",
            "url": "http://x.com",
            "abstract": "Abstract",
            "authors": "Author",
            "date": "2026-01-01",
        }
        save_paper(paper, "Cached summary", "KW")
        result = summarize_paper(paper, "KW")
        assert result == "Cached summary"
        mock_openai_client.chat.completions.create.assert_not_called()

    @patch("research_agent.time.sleep")
    @patch("research_agent.client")
    def test_summarize_retries_on_failure(self, mock_openai_client, mock_sleep):
        from research_agent import summarize_paper
        mock_openai_client.chat.completions.create.side_effect = [
            Exception("API error"),
            Exception("API error again"),
            Exception("API error third"),
        ]
        paper = {
            "id": "retry_test",
            "title": "Retry",
            "url": "http://x.com",
            "abstract": "Abstract",
            "authors": "Author",
            "date": "2026-01-01",
        }
        result = summarize_paper(paper, "KW")
        assert "失败" in result
        assert mock_openai_client.chat.completions.create.call_count == 3
