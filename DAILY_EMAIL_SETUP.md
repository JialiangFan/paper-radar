# 每日邮件推送服务设置指南

本文档说明如何设置和管理两个每日邮件推送服务：
1. **daily_tv_speaking_email** - 每日英语口语练习邮件（TV 对话片段）
2. **daily_news_email** - 每日新闻摘要邮件

## 服务概览

### daily_tv_speaking_email
- **功能**: 每天发送包含 TV 剧集对话片段的英语口语练习邮件
- **数据源**: OpenSubtitles.com API
- **运行时间**: 每天美东时间 12:30 AM

### daily_news_email
- **功能**: 每天发送最新新闻摘要邮件
- **数据源**: NewsAPI.org
- **运行时间**: 每天美东时间 12:30 AM

## 安装和配置

### 1. 安装依赖

```bash
# TV Speaking Email
cd /home/ubuntu/research_agent/daily_tv_speaking_email
pip3 install -r requirements.txt

# News Email
cd /home/ubuntu/research_agent/daily_news_email
pip3 install -r requirements.txt
```

### 2. 配置 API 密钥

#### OpenSubtitles API (TV Speaking Email)

1. 在 [OpenSubtitles.com](https://www.opensubtitles.com/) 注册账号
2. 在 API 设置中创建 API key
3. 设置环境变量（推荐在 `.env` 文件中）：

```bash
cd /home/ubuntu/research_agent/daily_tv_speaking_email
cat > .env << EOF
OS_API_KEY=your-opensubtitles-api-key
OS_USERNAME=your-username  # 可选，但推荐
OS_PASSWORD=your-password   # 可选，但推荐
EOF
chmod 600 .env
```

#### NewsAPI (News Email)

1. 在 [NewsAPI.org](https://newsapi.org/) 注册账号
2. 获取免费 API key（每天 100 次请求）
3. 设置环境变量（推荐在 `.env` 文件中）：

```bash
cd /home/ubuntu/research_agent/daily_news_email
cat > .env << EOF
NEWS_API_KEY=your-newsapi-key
EOF
chmod 600 .env
```

### 3. 配置邮件设置

两个服务都使用相同的邮件配置方式：

#### 方式 1: 使用 Mailgun API（推荐）

```bash
export USE_MAILGUN_API=true
export MAILGUN_API_KEY=your-mailgun-api-key
export MAILGUN_DOMAIN=mg.yourdomain.com
```

#### 方式 2: 使用 SMTP

编辑配置文件 `config.yaml`：

```yaml
email:
  from: "Your Name <noreply@yourdomain.com>"
  to:
    - "recipient@example.com"
  smtp_host: "smtp.mailgun.org"
  smtp_port: 587
  smtp_user: "postmaster@mg.yourdomain.com"
  smtp_password: "your-smtp-password"
```

### 4. 配置文件位置

- **TV Speaking Email**: `/home/ubuntu/research_agent/daily_tv_speaking_email/config.yaml`
- **News Email**: `/home/ubuntu/research_agent/daily_news_email/config.yaml`

## Systemd 服务管理

### 服务文件位置

所有服务文件已安装到 `/etc/systemd/system/`：

- `daily-tv-speaking-email.service` - TV 口语邮件服务
- `daily-tv-speaking-email.timer` - TV 口语邮件定时器
- `daily-news-email.service` - 新闻邮件服务
- `daily-news-email.timer` - 新闻邮件定时器

### 启用定时器

```bash
# 启用 TV Speaking Email 定时器
sudo systemctl enable daily-tv-speaking-email.timer
sudo systemctl start daily-tv-speaking-email.timer

# 启用 News Email 定时器
sudo systemctl enable daily-news-email.timer
sudo systemctl start daily-news-email.timer
```

### 查看定时器状态

```bash
# 查看所有定时器
sudo systemctl list-timers daily-*.timer

# 查看特定定时器状态
sudo systemctl status daily-tv-speaking-email.timer
sudo systemctl status daily-news-email.timer
```

### 手动运行服务（测试）

```bash
# 测试 TV Speaking Email（dry-run）
cd /home/ubuntu/research_agent/daily_tv_speaking_email
python3 -m daily_tv_speaking_email run --config config.yaml --dry-run --debug

# 测试 News Email（dry-run）
cd /home/ubuntu/research_agent/daily_news_email
python3 -m daily_news_email run --config config.yaml --dry-run --debug

# 手动触发服务（实际发送）
sudo systemctl start daily-tv-speaking-email.service
sudo systemctl start daily-news-email.service
```

### 查看日志

```bash
# TV Speaking Email 日志
sudo journalctl -u daily-tv-speaking-email.service -f

# News Email 日志
sudo journalctl -u daily-news-email.service -f

# 查看最近的日志
sudo journalctl -u daily-tv-speaking-email.service -n 50
sudo journalctl -u daily-news-email.service -n 50
```

## 定时设置

两个服务都设置为每天美东时间 12:30 AM（00:30）运行。

定时器配置使用 `America/New_York` 时区，会自动处理 EST/EDT 转换。

### 修改运行时间

编辑定时器文件：

```bash
sudo systemctl edit daily-tv-speaking-email.timer
sudo systemctl edit daily-news-email.timer
```

或者直接编辑：

```bash
sudo nano /etc/systemd/system/daily-news-email.timer
```

修改 `OnCalendar` 行，例如改为每天早上 8:00：

```ini
OnCalendar=*-*-* 08:00:00 America/New_York
```

然后重新加载：

```bash
sudo systemctl daemon-reload
sudo systemctl restart daily-news-email.timer
```

## 故障排除

### 1. 服务无法启动

检查服务状态：

```bash
sudo systemctl status daily-news-email.service
```

查看详细错误：

```bash
sudo journalctl -u daily-news-email.service -n 100
```

### 2. API 密钥问题

确保环境变量已设置：

```bash
# 检查环境变量
env | grep -E "(OS_API_KEY|NEWS_API_KEY)"

# 测试 API 连接
cd /home/ubuntu/research_agent/daily_news_email
python3 -m daily_news_email run --config config.yaml --dry-run --debug
```

### 3. 邮件发送失败

测试邮件配置：

```bash
# 测试 TV Speaking Email 邮件
cd /home/ubuntu/research_agent/daily_tv_speaking_email
python3 -m daily_tv_speaking_email test-email --config config.yaml --debug

# 测试 News Email 邮件
cd /home/ubuntu/research_agent/daily_news_email
python3 -m daily_news_email test-email --config config.yaml --debug
```

### 4. 定时器未触发

检查定时器状态：

```bash
sudo systemctl status daily-news-email.timer
```

查看下次运行时间：

```bash
sudo systemctl list-timers daily-*.timer
```

## 环境变量参考

### TV Speaking Email

- `OS_API_KEY` - OpenSubtitles API key（必需）
- `OS_USERNAME` - OpenSubtitles 用户名（可选）
- `OS_PASSWORD` - OpenSubtitles 密码（可选）
- `USE_MAILGUN_API` - 是否使用 Mailgun（true/false）
- `MAILGUN_API_KEY` - Mailgun API key
- `MAILGUN_DOMAIN` - Mailgun 域名
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` - SMTP 配置
- `EMAIL_FROM`, `EMAIL_TO` - 邮件地址

### News Email

- `NEWS_API_KEY` - NewsAPI key（必需）
- `NEWS_COUNTRY` - 国家代码（默认: "us"）
- `NEWS_LANGUAGE` - 语言代码（默认: "en"）
- `NEWS_CATEGORY` - 新闻类别（可选）
- `NEWS_QUERY` - 搜索查询（可选）
- `NEWS_MAX_ARTICLES` - 最大文章数（默认: 10）
- `USE_MAILGUN_API` - 是否使用 Mailgun（true/false）
- `MAILGUN_API_KEY` - Mailgun API key
- `MAILGUN_DOMAIN` - Mailgun 域名
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` - SMTP 配置
- `EMAIL_FROM`, `EMAIL_TO` - 邮件地址

## 文件结构

```
/home/ubuntu/research_agent/
├── daily_tv_speaking_email/
│   ├── daily_tv_speaking_email/
│   │   ├── __main__.py
│   │   ├── config.py
│   │   ├── mailer.py
│   │   └── ...
│   ├── config.yaml
│   ├── requirements.txt
│   ├── daily-tv-speaking-email.service
│   └── daily-tv-speaking-email.timer
├── daily_news_email/
│   ├── daily_news_email/
│   │   ├── __main__.py
│   │   ├── config.py
│   │   ├── mailer.py
│   │   ├── news_client.py
│   │   └── ...
│   ├── config.yaml
│   ├── requirements.txt
│   ├── daily-news-email.service
│   └── daily-news-email.timer
└── DAILY_EMAIL_SETUP.md (本文件)
```

## 下一步

1. 设置 API 密钥（OpenSubtitles 和 NewsAPI）
2. 配置邮件设置（Mailgun 或 SMTP）
3. 测试服务（使用 `--dry-run` 模式）
4. 启用并启动定时器
5. 监控日志确保正常运行

## 相关文档

- [daily_tv_speaking_email README](daily_tv_speaking_email/README.md)
- [daily_news_email README](daily_news_email/README.md)
- [EMAIL_CONFIG.md](EMAIL_CONFIG.md) - 邮件配置详细说明
