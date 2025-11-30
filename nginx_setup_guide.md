# Research Agent Nginx SSL 配置指南

## 步骤 1: 获取 SSL 证书（使用 Let's Encrypt）

### 安装 Certbot

```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx -y
```

### 获取 SSL 证书

```bash
# 替换 your-domain.com 为你的实际域名
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

Certbot 会自动：
- 获取 SSL 证书
- 配置 nginx
- 设置自动续期

## 步骤 2: 配置 Nginx

### 1. 编辑配置文件

```bash
# 复制配置文件到 nginx 配置目录
sudo cp nginx_research_agent.conf /etc/nginx/sites-available/research_agent

# 编辑配置文件，替换域名和证书路径
sudo nano /etc/nginx/sites-available/research_agent
```

**重要：需要修改以下内容：**
- `server_name`: 替换为你的实际域名
- `ssl_certificate`: 替换为实际的证书路径
- `ssl_certificate_key`: 替换为实际的私钥路径
- `ssl_trusted_certificate`: 替换为实际的链证书路径

### 2. 启用配置

```bash
# 创建符号链接启用配置
sudo ln -s /etc/nginx/sites-available/research_agent /etc/nginx/sites-enabled/

# 测试 nginx 配置
sudo nginx -t

# 如果测试通过，重新加载 nginx
sudo systemctl reload nginx
```

## 步骤 3: 确保 Research Agent Web UI 正在运行

确保 Web UI 在后台运行（端口 5001）：

```bash
# 使用 systemd 服务（推荐）
# 或者使用 screen/tmux
screen -S research_agent
cd /home/ubuntu/research_agent
./start_web_ui.sh
# 按 Ctrl+A 然后 D 来 detach

# 或者使用 nohup
cd /home/ubuntu/research_agent
nohup ./start_web_ui.sh > web_ui.log 2>&1 &
```

## 步骤 4: 防火墙配置

确保防火墙允许 HTTP 和 HTTPS 流量：

```bash
# 如果使用 ufw
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw reload

# 如果使用 iptables
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

## 步骤 5: 验证配置

1. 访问 `http://your-domain.com` - 应该自动重定向到 HTTPS
2. 访问 `https://your-domain.com` - 应该看到 Research Agent Web UI
3. 检查浏览器地址栏的 SSL 锁图标

## 故障排除

### 检查 nginx 状态
```bash
sudo systemctl status nginx
```

### 查看 nginx 错误日志
```bash
sudo tail -f /var/log/nginx/research_agent_error.log
```

### 检查 Web UI 是否运行
```bash
curl http://localhost:5001
```

### 测试 SSL 配置
```bash
sudo nginx -t
```

## 自动续期

Let's Encrypt 证书每 90 天需要续期。Certbot 会自动设置定时任务，但你可以手动测试：

```bash
sudo certbot renew --dry-run
```

## 注意事项

1. **域名 DNS 配置**: 确保域名正确指向服务器 IP
2. **端口开放**: 确保 80 和 443 端口在防火墙中开放
3. **Web UI 运行**: 确保 Research Agent Web UI 在 localhost:5001 运行
4. **证书路径**: 如果使用自定义证书，确保路径正确且权限正确
