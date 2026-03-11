# Research Agent

> **[中文版](#中文版) | English**

An AI-powered academic paper tracking system that automatically fetches papers from ArXiv, generates summaries using OpenAI, and delivers daily email digests. Includes a modern Web UI and subscriber management.

## Live Demo

**[zhatgpt.com](https://zhatgpt.com)**

[![Website Preview](https://api.microlink.io/?url=https%3A%2F%2Fzhatgpt.com&screenshot=true&meta=false&embed=screenshot.url)](https://zhatgpt.com)

## Features

- **ArXiv Search**: Keyword and author-based paper discovery with smart deduplication
- **AI Summarization**: Structured summaries via OpenAI with caching to reduce API costs
- **Email Delivery**: Automated daily digests via Mailgun API or SMTP fallback
- **Web UI**: FastAPI-based interface for keyword management, search, and paper browsing
- **Subscriber System**: Email subscription with one-click unsubscribe
- **Data Export**: Export papers to CSV
- **Scheduling**: Built-in scheduler (daily 9:00 AM ET) or systemd/cron integration

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp env.example .env
# Edit .env with your API keys and email settings
```

**Required environment variables:**

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key for paper summarization |
| `EMAIL_SENDER` | Sender email address |
| `EMAIL_RECEIVER` | Default recipient email address |

**Optional (Mailgun — recommended):**

| Variable | Description |
|----------|-------------|
| `USE_MAILGUN_API` | Set to `true` to enable Mailgun |
| `MAILGUN_API_KEY` | Your Mailgun API key |
| `MAILGUN_DOMAIN` | Your Mailgun domain |

**Optional (SMTP fallback):**

| Variable | Default | Description |
|----------|---------|-------------|
| `SMTP_SERVER` | `localhost` | SMTP server address |
| `SMTP_PORT` | `25` | Port (25/587/465) |
| `SMTP_USE_SSL` | `false` | Enable SSL (port 465) |
| `SMTP_USE_TLS` | `true` | Enable TLS (port 587) |
| `EMAIL_PASSWORD` | — | SMTP password |

### 3. Configure keywords

Edit `keywords.txt` (one keyword per line, `#` for comments):

```
Large Language Models
Agentic Workflow
# comments are ignored
```

### 4. Run

```bash
# One-time execution
python research_agent.py

# Start Web UI (http://localhost:5001)
python web_ui.py

# Start daily scheduler (9:00 AM ET)
python research_agent.py schedule
```

## Web UI

Start with `python web_ui.py`, then open **http://localhost:5001**.

**Capabilities:**
- Manage keywords (add/delete)
- Search papers by keyword or author
- Browse saved papers with AI summaries
- Export to CSV
- Manage email subscriptions

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/keywords` | List keywords |
| `POST` | `/api/keywords` | Add keyword |
| `DELETE` | `/api/keywords/{index}` | Delete keyword |
| `POST` | `/api/search` | Search by keyword |
| `POST` | `/api/search_by_author` | Search by author |
| `GET` | `/api/papers` | Get saved papers |
| `GET` | `/api/papers/all` | Get all papers with stats |
| `GET` | `/api/papers/export/csv` | Export CSV |
| `POST` | `/api/subscribe` | Subscribe to mailing list |
| `POST` | `/api/unsubscribe` | Unsubscribe |
| `GET` | `/api/unsubscribe/{token}` | Token-based unsubscribe |

## Database

Uses SQLite (`papers.db`) with automatic environment-based separation:

| `APP_ENV` | Database File |
|-----------|--------------|
| `production` (default) | `papers.db` |
| `development` | `papers.dev.db` |
| `test` | `papers.test.db` |

Set `DATABASE_PATH` to override with a custom path.

## Production Deployment

### Systemd service

```bash
./setup_systemd_service.sh
```

### Nginx reverse proxy

```bash
./setup_nginx.sh
```

### Cron job

```bash
crontab -e
# Add: 0 10 * * * cd /path/to/research_agent && python research_agent.py
```

## Supplementary Services

### Daily News Email (`daily_news_email/`)

Fetches articles from NewsAPI and sends daily news digests. Requires `NEWS_API_KEY`.

```bash
pip install -r daily_news_email/requirements.txt
cp daily_news_email/config.example.yaml daily_news_email/config.yaml
python -m daily_news_email
```

### Daily TV Speaking Email (`daily_tv_speaking_email/`)

Extracts TV dialogue snippets for English speaking practice. Requires `OS_API_KEY` (OpenSubtitles).

```bash
pip install -r daily_tv_speaking_email/requirements.txt
cp daily_tv_speaking_email/config.example.yaml daily_tv_speaking_email/config.yaml
python -m daily_tv_speaking_email
```

## Project Structure

```
research_agent/
├── research_agent.py          # Core: fetching, summarization, email
├── web_ui.py                  # FastAPI web server
├── templates/index.html       # Web UI frontend
├── keywords.txt               # Search keywords
├── requirements.txt           # Python dependencies
├── .env                       # Environment config (not tracked)
├── daily_news_email/          # News digest service
└── daily_tv_speaking_email/   # TV speaking practice service
```

## Documentation

- [Email Configuration Guide](EMAIL_CONFIG.md)
- [Mailgun Setup Guide](MAILGUN_CONFIG.md)
- [Web UI Guide](WEB_UI_GUIDE.md)
- [Daily Email Services Setup](DAILY_EMAIL_SETUP.md)
- [Systemd Service Guide](systemd_service_guide.md)
- [Nginx Setup Guide](nginx_setup_guide.md)

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=JFan5/research_agent&type=Date)](https://star-history.com/#JFan5/research_agent&Date)

---

<a name="中文版"></a>

# Research Agent - ArXiv 论文日报

> **中文 | [English](#research-agent)**

自动从 ArXiv 抓取最新论文，使用 AI 总结，并发送邮件日报。

## 在线演示

**[zhatgpt.com](https://zhatgpt.com)**

[![网站预览](https://api.microlink.io/?url=https%3A%2F%2Fzhatgpt.com&screenshot=true&meta=false&embed=screenshot.url)](https://zhatgpt.com)

## 功能特性

- **ArXiv 搜索**：根据关键词或作者自动搜索，智能去重
- **AI 总结**：通过 OpenAI 生成结构化摘要，带缓存减少 API 开销
- **邮件推送**：通过 Mailgun API 或 SMTP 自动发送每日邮件
- **Web UI**：基于 FastAPI 的界面，支持关键词管理、搜索和论文浏览
- **订阅系统**：邮件订阅，一键退订
- **数据导出**：导出论文为 CSV
- **定时任务**：内置调度器（每天美东时间 9:00）或 systemd/cron 集成

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp env.example .env
# 编辑 .env 填入 API 密钥和邮件配置
```

**必需环境变量：**

| 变量 | 说明 |
|------|------|
| `OPENAI_API_KEY` | OpenAI API 密钥 |
| `EMAIL_SENDER` | 发件人邮箱 |
| `EMAIL_RECEIVER` | 默认收件人邮箱 |

**可选（Mailgun，推荐）：**

| 变量 | 说明 |
|------|------|
| `USE_MAILGUN_API` | 设为 `true` 启用 Mailgun |
| `MAILGUN_API_KEY` | Mailgun API 密钥 |
| `MAILGUN_DOMAIN` | Mailgun 域名 |

**可选（SMTP 备选）：**

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `SMTP_SERVER` | `localhost` | SMTP 服务器地址 |
| `SMTP_PORT` | `25` | 端口 (25/587/465) |
| `SMTP_USE_SSL` | `false` | 启用 SSL (465) |
| `SMTP_USE_TLS` | `true` | 启用 TLS (587) |
| `EMAIL_PASSWORD` | — | SMTP 密码 |

### 3. 配置关键词

编辑 `keywords.txt`（每行一个关键词，`#` 为注释）：

```
Large Language Models
Agentic Workflow
# 注释会被忽略
```

### 4. 运行

```bash
# 手动运行一次
python research_agent.py

# 启动 Web UI（http://localhost:5001）
python web_ui.py

# 启动定时任务（美东时间 9:00）
python research_agent.py schedule
```

## Web UI

运行 `python web_ui.py` 后访问 **http://localhost:5001**。

**功能：**
- 管理关键词（添加/删除）
- 按关键词或作者搜索论文
- 浏览已保存论文及 AI 总结
- 导出 CSV
- 管理邮件订阅

## 数据库

使用 SQLite（`papers.db`），按环境自动切换：

| `APP_ENV` | 数据库文件 |
|-----------|-----------|
| `production`（默认） | `papers.db` |
| `development` | `papers.dev.db` |
| `test` | `papers.test.db` |

设置 `DATABASE_PATH` 可自定义路径。

## 生产部署

```bash
# Systemd 服务
./setup_systemd_service.sh

# Nginx 反向代理
./setup_nginx.sh

# Cron 定时任务
crontab -e
# 添加: 0 10 * * * cd /path/to/research_agent && python research_agent.py
```

## 附加服务

- **`daily_news_email/`**：每日新闻摘要邮件（需要 `NEWS_API_KEY`）
- **`daily_tv_speaking_email/`**：英语口语练习邮件（需要 `OS_API_KEY`）

## 文件说明

```
research_agent/
├── research_agent.py          # 核心：抓取、总结、邮件
├── web_ui.py                  # FastAPI Web 服务器
├── templates/index.html       # Web UI 前端
├── keywords.txt               # 搜索关键词
├── requirements.txt           # Python 依赖
├── .env                       # 环境配置（不跟踪）
├── daily_news_email/          # 新闻摘要服务
└── daily_tv_speaking_email/   # 口语练习服务
```

## 相关文档

- [邮件配置指南](EMAIL_CONFIG.md)
- [Mailgun 配置指南](MAILGUN_CONFIG.md)
- [Web UI 使用指南](WEB_UI_GUIDE.md)
- [每日邮件服务配置](DAILY_EMAIL_SETUP.md)
- [Systemd 服务指南](systemd_service_guide.md)
- [Nginx 配置指南](nginx_setup_guide.md)

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=JFan5/research_agent&type=Date)](https://star-history.com/#JFan5/research_agent&Date)
