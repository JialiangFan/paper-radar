# Research Agent 邮件配置指南

## 概述

Research Agent 现在支持通过SMTP服务器发送邮件，可以使用服务器的邮件服务和域名。所有邮件配置都通过环境变量管理，确保安全性和灵活性。

## 配置文件位置

- **环境变量文件**: `/home/ubuntu/research_agent/.env`
- **Systemd 服务文件**: `/etc/systemd/system/research-agent-web.service`

## 配置方法

### 方法 1: 使用配置脚本（推荐）

```bash
cd /home/ubuntu/research_agent
./configure_email.sh
```

脚本会引导你输入：
- 发送邮箱（使用你的域名邮箱）
- SMTP服务器地址
- SMTP端口
- SSL/TLS配置
- SMTP密码（如果需要认证）
- 接收邮箱

### 方法 2: 手动编辑 .env 文件

```bash
cd /home/ubuntu/research_agent
nano .env
```

编辑以下配置：

```bash
# 邮件配置 - SMTP服务器
EMAIL_SENDER=sender@yourdomain.com
EMAIL_PASSWORD=your_smtp_password_here
EMAIL_RECEIVER=recipient@example.com

# SMTP服务器配置
SMTP_SERVER=localhost
SMTP_PORT=25
SMTP_USE_SSL=false
SMTP_USE_TLS=true
EMAIL_SENDER_NAME=Research Agent
```

保存后重启服务：

```bash
sudo systemctl restart research-agent-web.service
```

## SMTP服务器配置说明

### 常见配置示例

#### 1. 本地SMTP服务器（Postfix/Sendmail）

```bash
SMTP_SERVER=localhost
SMTP_PORT=25
SMTP_USE_SSL=false
SMTP_USE_TLS=false
EMAIL_PASSWORD=  # 留空，本地服务器通常不需要认证
```

#### 2. 标准SMTP服务器（端口25，可选TLS）

```bash
SMTP_SERVER=mail.yourdomain.com
SMTP_PORT=25
SMTP_USE_SSL=false
SMTP_USE_TLS=true
EMAIL_PASSWORD=your_password
```

#### 3. 安全SMTP服务器（端口587，TLS）

```bash
SMTP_SERVER=mail.yourdomain.com
SMTP_PORT=587
SMTP_USE_SSL=false
SMTP_USE_TLS=true
EMAIL_PASSWORD=your_password
```

#### 4. 安全SMTP服务器（端口465，SSL）

```bash
SMTP_SERVER=mail.yourdomain.com
SMTP_PORT=465
SMTP_USE_SSL=true
SMTP_USE_TLS=false
EMAIL_PASSWORD=your_password
```

### 配置参数说明

- **SMTP_SERVER**: SMTP服务器地址
  - 本地服务器: `localhost` 或 `127.0.0.1`
  - 远程服务器: `mail.yourdomain.com` 或 `smtp.yourdomain.com`

- **SMTP_PORT**: SMTP端口
  - `25`: 标准SMTP端口（通常需要TLS）
  - `587`: 提交端口（通常使用TLS）
  - `465`: SSL端口（使用SSL）

- **SMTP_USE_SSL**: 是否使用SSL连接
  - `true`: 使用SSL（端口通常为465）
  - `false`: 不使用SSL（默认）

- **SMTP_USE_TLS**: 是否使用TLS加密
  - `true`: 使用TLS（推荐，端口通常为587或25）
  - `false`: 不使用TLS（仅用于本地或内网）

- **EMAIL_PASSWORD**: SMTP认证密码
  - 如果服务器需要认证，填写密码
  - 如果留空，将跳过认证（仅适用于本地SMTP服务器）

- **EMAIL_SENDER_NAME**: 发件人显示名称（可选）
  - 默认: `Research Agent`

## 环境变量优先级

配置读取优先级（从高到低）：
1. **系统环境变量** - 通过 `export` 命令设置
2. **.env 文件** - `/home/ubuntu/research_agent/.env`
3. **默认值** - 代码中的默认值

## Systemd 服务配置

服务会自动从 `.env` 文件加载环境变量：

```ini
[Service]
EnvironmentFile=/home/ubuntu/research_agent/.env
```

这意味着：
- 服务启动时会自动加载 `.env` 文件中的所有环境变量
- 修改 `.env` 文件后需要重启服务才能生效
- 系统环境变量的优先级高于 `.env` 文件

## 测试邮件发送

### 使用测试脚本

```bash
cd /home/ubuntu/research_agent
python3 test_email.py
```

### 手动测试

```python
from research_agent import send_email
send_email("<h1>测试邮件</h1><p>这是一封测试邮件。</p>")
```

## 验证配置

检查当前配置是否已加载：

```bash
cd /home/ubuntu/research_agent
python3 -c "
from research_agent import (
    EMAIL_SENDER, EMAIL_RECEIVER, SMTP_SERVER, SMTP_PORT,
    SMTP_USE_SSL, SMTP_USE_TLS
)
print(f'发送邮箱: {EMAIL_SENDER}')
print(f'接收邮箱: {EMAIL_RECEIVER}')
print(f'SMTP服务器: {SMTP_SERVER}:{SMTP_PORT}')
print(f'使用SSL: {SMTP_USE_SSL}')
print(f'使用TLS: {SMTP_USE_TLS}')
print(f'密码: {\"已设置\" if EMAIL_PASSWORD else \"未设置\"}')"
```

## 服务管理

### 重启服务以应用新配置

```bash
sudo systemctl restart research-agent-web.service
```

### 查看服务状态

```bash
sudo systemctl status research-agent-web.service
```

### 查看服务日志

```bash
sudo journalctl -u research-agent-web.service -f
```

## 安全建议

1. **保护 .env 文件**：
   ```bash
   chmod 600 /home/ubuntu/research_agent/.env
   ```

2. **不要将 .env 文件提交到 Git**：
   - `.env` 文件已添加到 `.gitignore`
   - 使用 `env.example` 作为模板

3. **使用TLS/SSL加密**：
   - 生产环境建议使用TLS（端口587）或SSL（端口465）
   - 避免在不安全的网络上传输明文密码

4. **定期更新密码**：
   - 如果怀疑密码泄露，立即更改SMTP密码

## 故障排除

### 邮件发送失败

1. **检查网络连接**：
   ```bash
   ping $SMTP_SERVER
   telnet $SMTP_SERVER $SMTP_PORT
   ```

2. **检查防火墙**：
   - 确保SMTP端口（25/587/465）未被阻止
   - 检查服务器防火墙规则

3. **验证SMTP配置**：
   - 确认SMTP服务器地址和端口正确
   - 确认SSL/TLS配置与服务器匹配
   - 确认用户名和密码正确

4. **查看日志**：
   ```bash
   sudo journalctl -u research-agent-web.service -n 50
   ```

5. **测试SMTP连接**：
   ```bash
   # 测试端口25
   telnet localhost 25
   
   # 测试端口587
   telnet mail.yourdomain.com 587
   
   # 测试端口465（需要SSL）
   openssl s_client -connect mail.yourdomain.com:465
   ```

### 环境变量未加载

1. **检查 .env 文件格式**：
   - 确保格式为 `KEY=VALUE`
   - 不要有多余的空格
   - 值不需要引号（除非包含特殊字符）

2. **检查服务配置**：
   ```bash
   sudo systemctl cat research-agent-web.service | grep EnvironmentFile
   ```

3. **重启服务**：
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl restart research-agent-web.service
   ```

### 常见错误

1. **"Connection refused"**:
   - SMTP服务器未运行或地址错误
   - 端口被防火墙阻止

2. **"Authentication failed"**:
   - 用户名或密码错误
   - SMTP服务器不支持该认证方式

3. **"SSL/TLS error"**:
   - SSL/TLS配置不匹配
   - 服务器证书问题

## 相关文件

- `/home/ubuntu/research_agent/.env` - 环境变量配置文件
- `/home/ubuntu/research_agent/configure_email.sh` - 配置管理脚本
- `/home/ubuntu/research_agent/test_email.py` - 邮件测试脚本
- `/home/ubuntu/research_agent/env.example` - 配置示例文件
- `/etc/systemd/system/research-agent-web.service` - Systemd 服务文件
