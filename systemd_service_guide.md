# Research Agent Web UI Systemd 服务配置指南

## 快速开始

运行自动化配置脚本：

```bash
cd /home/ubuntu/research_agent
sudo ./setup_systemd_service.sh
```

脚本会自动：
- 检测 conda 环境（paper_agent 或 base）
- 创建并配置 systemd 服务
- 启用开机自启
- 启动服务

## 手动配置

### 1. 复制服务文件

```bash
sudo cp research-agent-web.service /etc/systemd/system/
```

### 2. 根据你的环境编辑服务文件

```bash
sudo nano /etc/systemd/system/research-agent-web.service
```

**重要配置项：**

- **User/Group**: 确保是运行服务的用户（默认 ubuntu）
- **WorkingDirectory**: 项目目录路径
- **ExecStart**: Python 执行命令
  - 如果使用 paper_agent 环境：`/home/ubuntu/miniconda3/bin/conda run -n paper_agent python /home/ubuntu/research_agent/web_ui.py`
  - 如果使用 base 环境：`/home/ubuntu/miniconda3/bin/python /home/ubuntu/research_agent/web_ui.py`
- **Environment**: 设置环境变量
  - `FLASK_DEBUG=False`: 生产环境关闭 debug
  - `FLASK_PORT=5001`: Web UI 端口

### 3. 重新加载 systemd

```bash
sudo systemctl daemon-reload
```

### 4. 启用服务（开机自启）

```bash
sudo systemctl enable research-agent-web.service
```

### 5. 启动服务

```bash
sudo systemctl start research-agent-web.service
```

### 6. 检查服务状态

```bash
sudo systemctl status research-agent-web.service
```

## 常用命令

### 查看服务状态
```bash
sudo systemctl status research-agent-web
```

### 查看实时日志
```bash
sudo journalctl -u research-agent-web -f
```

### 查看最近日志
```bash
sudo journalctl -u research-agent-web -n 50
```

### 重启服务
```bash
sudo systemctl restart research-agent-web
```

### 停止服务
```bash
sudo systemctl stop research-agent-web
```

### 启动服务
```bash
sudo systemctl start research-agent-web
```

### 禁用开机自启
```bash
sudo systemctl disable research-agent-web
```

### 启用开机自启
```bash
sudo systemctl enable research-agent-web
```

## 故障排除

### 服务无法启动

1. **查看详细日志**：
```bash
sudo journalctl -u research-agent-web -n 100 --no-pager
```

2. **检查 Python 路径**：
```bash
# 测试 conda 环境
/home/ubuntu/miniconda3/bin/conda run -n paper_agent python --version

# 或测试 base 环境
/home/ubuntu/miniconda3/bin/python --version
```

3. **手动测试运行**：
```bash
cd /home/ubuntu/research_agent
source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate paper_agent  # 或 base
python web_ui.py
```

### 服务启动但无法访问

1. **检查端口是否监听**：
```bash
sudo netstat -tlnp | grep 5001
# 或
sudo ss -tlnp | grep 5001
```

2. **检查防火墙**：
```bash
sudo ufw status
```

3. **检查 nginx 配置**（如果使用 nginx）：
```bash
sudo nginx -t
sudo systemctl status nginx
```

### 服务频繁重启

1. **查看错误日志**：
```bash
sudo journalctl -u research-agent-web -n 100 | grep -i error
```

2. **检查依赖**：
```bash
# 确保所有依赖已安装
cd /home/ubuntu/research_agent
pip list
```

3. **检查环境变量**：
```bash
# 查看服务配置的环境变量
sudo systemctl show research-agent-web | grep Environment
```

## 生产环境优化

### 使用 Gunicorn（推荐）

对于生产环境，建议使用 Gunicorn 而不是直接运行 Flask：

1. **安装 Gunicorn**：
```bash
conda activate paper_agent  # 或 base
pip install gunicorn
```

2. **修改服务文件 ExecStart**：
```bash
ExecStart=/home/ubuntu/miniconda3/bin/conda run -n paper_agent gunicorn -w 4 -b 0.0.0.0:5001 --timeout 120 web_ui:app
```

### 性能调优

在服务文件中可以添加：
```ini
# 限制资源使用
LimitNOFILE=65536
MemoryLimit=2G
CPUQuota=200%
```

## 注意事项

1. **环境变量**: 确保 `OPENAI_API_KEY`、`EMAIL_SENDER` 等环境变量已设置
2. **文件权限**: 确保服务用户有权限访问项目目录和数据库文件
3. **日志轮转**: systemd 会自动管理日志，但可以配置日志大小限制
4. **自动重启**: 服务配置了 `Restart=always`，崩溃后会自动重启

## 验证服务运行

```bash
# 检查服务状态
sudo systemctl is-active research-agent-web

# 测试 Web UI
curl http://localhost:5001

# 检查进程
ps aux | grep web_ui.py
```
