# Mailgun API 配置指南

## 概述

Research Agent 现在支持使用 Mailgun Python API 发送邮件，这是推荐的邮件发送方式，可以避免端口25被阻止的问题。

## 需要的配置信息

要使用 Mailgun API，你需要提供以下信息：

1. **MAILGUN_API_KEY**: Mailgun API密钥
2. **MAILGUN_DOMAIN**: Mailgun域名（例如：`mg.yourdomain.com` 或 `yourdomain.com`）

## 如何获取 Mailgun 配置信息

### 1. 登录 Mailgun 控制台
访问：https://app.mailgun.com/

### 2. 获取 API Key
1. 登录后，点击右上角的 **Settings** → **API Keys**
2. 找到 **Private API key**，点击 **Reveal** 显示密钥
3. 复制这个 API Key（格式类似：`key-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`）

### 3. 获取 Domain
1. 在 Mailgun 控制台中，进入 **Sending** → **Domains**
2. 找到你的域名（例如：`mg.yourdomain.com` 或 `yourdomain.com`）
3. 复制域名名称

**注意**：
- 如果域名还没添加，需要先添加并验证域名
- 域名格式通常是 `mg.yourdomain.com` 或直接使用 `yourdomain.com`

## 配置步骤

### 方法 1: 使用配置脚本（推荐）

```bash
cd /path/to/research_agent
./configure_email.sh
```

### 方法 2: 手动编辑 .env 文件

编辑 `/path/to/research_agent/.env` 文件，添加以下配置：

```bash
# 邮件配置
EMAIL_SENDER=noreply@yourdomain.com
EMAIL_RECEIVER=REDACTED_EMAIL
EMAIL_SENDER_NAME=Research Agent

# Mailgun API 配置
USE_MAILGUN_API=true
MAILGUN_API_KEY=your_mailgun_api_key_here
MAILGUN_DOMAIN=mg.yourdomain.com
```

**重要**：
- 设置 `USE_MAILGUN_API=true` 来启用 Mailgun API
- `MAILGUN_DOMAIN` 应该是你在 Mailgun 中配置的域名（例如：`mg.yourdomain.com`）

## 测试配置

配置完成后，运行测试脚本：

```bash
cd /path/to/research_agent
python3 test_email.py
```

如果配置正确，你应该看到：
```
✅ 邮件发送成功！请检查收件箱（包括垃圾邮件文件夹）。
```

## 验证配置

检查当前配置：

```bash
cd /path/to/research_agent
python3 -c "
from research_agent import load_env_file, USE_MAILGUN_API, MAILGUN_DOMAIN, EMAIL_SENDER, EMAIL_RECEIVER
load_env_file()
print(f'使用Mailgun API: {USE_MAILGUN_API}')
print(f'Mailgun Domain: {MAILGUN_DOMAIN}')
print(f'发件人: {EMAIL_SENDER}')
print(f'收件人: {EMAIL_RECEIVER}')
"
```

## 工作原理

- 当 `USE_MAILGUN_API=true` 时，系统会使用 Mailgun REST API 发送邮件
- 如果 Mailgun API 失败，会自动回退到 SMTP 方式（如果配置了）
- Mailgun API 使用 HTTPS 连接，不受端口25限制影响

## 故障排除

### 邮件发送失败

1. **检查 API Key**：
   ```bash
   # 验证 API Key 是否正确
   curl -s --user "api:YOUR_API_KEY" \
     https://api.mailgun.net/v3/domains/YOUR_DOMAIN
   ```

2. **检查域名**：
   - 确保域名在 Mailgun 中已验证
   - 确保域名格式正确（例如：`mg.yourdomain.com`）

3. **查看错误信息**：
   - 运行 `python3 test_email.py` 查看详细错误信息
   - Mailgun API 错误会显示 HTTP 状态码和错误消息

### 常见错误

- **401 Unauthorized**: API Key 错误或无效
- **404 Not Found**: Domain 不存在或格式错误
- **403 Forbidden**: 域名未验证或账户权限问题

## 相关文件

- `/path/to/research_agent/.env` - 环境变量配置文件
- `/path/to/research_agent/research_agent.py` - 主程序（包含Mailgun API实现）
- `/path/to/research_agent/test_email.py` - 邮件测试脚本
