# Mailgun 邮件服务配置指南

## 需要的配置信息

要使用 Mailgun 发送邮件，你需要提供以下信息：

### 1. Mailgun 账户信息
- **SMTP 用户名**：通常是 `REDACTED_SMTP_USER` 或类似格式
- **SMTP 密码**：Mailgun 提供的 SMTP 密码（不是 API Key）
- **SMTP 服务器**：`smtp.mailgun.org`
- **SMTP 端口**：`587` (推荐，使用 TLS) 或 `465` (使用 SSL)

### 2. 如何获取 Mailgun 配置信息

1. **登录 Mailgun 控制台**：https://app.mailgun.com/
2. **选择你的域名**：`yourdomain.com`（如果没有添加，需要先添加域名）
3. **进入域名设置**：点击域名 → "Sending" → "SMTP credentials"
4. **获取 SMTP 信息**：
   - SMTP Username: 通常是 `REDACTED_SMTP_USER`
   - SMTP Password: 点击 "Reset Password" 生成新密码
   - SMTP Hostname: `smtp.mailgun.org`
   - Port: `587` (TLS) 或 `465` (SSL)

### 3. 域名验证（如果还没完成）

如果域名 `yourdomain.com` 还没在 Mailgun 中验证，需要：
1. 添加域名到 Mailgun
2. 添加 DNS 记录（MX, TXT, CNAME）
3. 等待验证完成

## 配置步骤

配置完成后，运行：
```bash
cd /path/to/research_agent
./configure_email.sh
```

或者直接编辑 `.env` 文件：
```bash
EMAIL_SENDER=noreply@yourdomain.com
EMAIL_PASSWORD=your_mailgun_smtp_password
EMAIL_RECEIVER=REDACTED_EMAIL

SMTP_SERVER=smtp.mailgun.org
SMTP_PORT=587
SMTP_USE_SSL=false
SMTP_USE_TLS=true
EMAIL_SENDER_NAME=Research Agent
```

## 测试

配置完成后测试：
```bash
python3 test_email.py
```
