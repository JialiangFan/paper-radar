# Research Agent - ArXiv 论文日报

自动从 ArXiv 抓取最新论文，使用 AI 总结，并发送邮件日报。

## 功能特性

- 🔍 根据关键词自动搜索 ArXiv 最新论文
- 🤖 使用 OpenAI API 生成中文总结
- 📧 自动发送 HTML 格式的邮件日报
- 🛡️ 包含错误处理、重试机制和去重功能
- 💾 **SQLite 数据库存储已抓取的论文**
- 🔄 **OpenAI 总结缓存，避免重复调用 API**
- ⏰ **定时任务：每天 10:00 自动运行**

## 安装

```bash
pip install -r requirements.txt
```

## 配置

### 1. 设置环境变量

#### 方法一：使用配置脚本（推荐）

```bash
cd /home/ubuntu/research_agent
./configure_email.sh
```

#### 方法二：手动配置

创建 `.env` 文件或设置环境变量：

```bash
# OpenAI API 配置
export OPENAI_API_KEY="your_openai_api_key"

# 邮件配置 - SMTP服务器
export EMAIL_SENDER="sender@yourdomain.com"
export EMAIL_PASSWORD="your_smtp_password"  # 如果SMTP服务器需要认证
export EMAIL_RECEIVER="recipient@example.com"

# SMTP服务器配置
export SMTP_SERVER="localhost"  # 或你的SMTP服务器地址
export SMTP_PORT="25"  # 25(标准), 587(TLS), 465(SSL)
export SMTP_USE_SSL="false"  # true 或 false
export SMTP_USE_TLS="true"  # true 或 false
export EMAIL_SENDER_NAME="Research Agent"
```

### 2. SMTP服务器配置说明

#### 常见配置示例

**本地SMTP服务器（Postfix/Sendmail）**：
```bash
SMTP_SERVER=localhost
SMTP_PORT=25
SMTP_USE_SSL=false
SMTP_USE_TLS=false
EMAIL_PASSWORD=  # 留空，本地服务器通常不需要认证
```

**标准SMTP服务器（端口25，TLS）**：
```bash
SMTP_SERVER=mail.yourdomain.com
SMTP_PORT=25
SMTP_USE_SSL=false
SMTP_USE_TLS=true
EMAIL_PASSWORD=your_password
```

**安全SMTP服务器（端口587，TLS）**：
```bash
SMTP_SERVER=mail.yourdomain.com
SMTP_PORT=587
SMTP_USE_SSL=false
SMTP_USE_TLS=true
EMAIL_PASSWORD=your_password
```

**安全SMTP服务器（端口465，SSL）**：
```bash
SMTP_SERVER=mail.yourdomain.com
SMTP_PORT=465
SMTP_USE_SSL=true
SMTP_USE_TLS=false
EMAIL_PASSWORD=your_password
```

详细配置说明请参考 [EMAIL_CONFIG.md](EMAIL_CONFIG.md)

### 3. 配置关键词（推荐）

编辑 `keywords.txt` 文件，每行一个关键词：

```txt
Large Language Models
Agentic Workflow
Transformer Architecture
```

**说明**：
- 每行一个关键词
- 空行会被自动忽略
- 以 `#` 开头的行会被视为注释，自动忽略
- 如果 `keywords.txt` 文件不存在或为空，程序会使用默认关键词

**示例 keywords.txt**：
```txt
# 这是我的关键词列表
Large Language Models
Agentic Workflow

# 也可以添加其他关键词
Computer Vision
```

## 使用方法

### 方式一：Web UI 界面（推荐）✨

启动 Web UI 服务器：

```bash
# 使用 Python 直接运行
python web_ui.py

# 或使用提供的脚本
./start_web_ui.sh
```

然后在浏览器中访问：**http://localhost:5001**

**Web UI 功能**：
- 📋 **关键词管理**：查看、添加、删除关键词
- 🔍 **主动搜索**：输入关键词立即搜索论文
- 📚 **论文展示**：查看已保存的论文和 AI 总结
- 💾 **自动保存**：搜索结果自动保存到数据库

### 方式二：手动运行一次

```bash
python research_agent.py
```

### 方式三：启动定时任务

```bash
# 使用 Python 直接运行
python research_agent.py schedule

# 或使用提供的脚本
./run_scheduler.sh
```

定时任务会在每天 **美东时间 09:00** 自动运行。程序会持续运行，按 `Ctrl+C` 退出。

**注意**：定时任务会自动处理美东时间的夏令时（EST/EDT）切换。

### 方式四：使用系统 cron（Linux/Mac）

编辑 crontab：

```bash
crontab -e
```

添加以下行（每天 10:00 运行）：

```bash
0 10 * * * cd /path/to/paper_agent && conda activate paper_agent && python research_agent.py
```

## 数据库

程序使用 SQLite 数据库 `papers.db` 存储：

- **已抓取的论文**：避免重复处理
- **OpenAI 总结缓存**：避免重复调用 API，节省成本

数据库表结构：
- `id`: 论文唯一标识（arXiv URL）
- `title`: 论文标题
- `url`: 论文链接
- `abstract`: 论文摘要
- `authors`: 作者列表
- `date`: 发布日期
- `summary`: OpenAI 生成的总结（缓存）
- `keyword`: 搜索关键词
- `created_at`: 创建时间
- `sent_at`: 发送时间

## 注意事项

- 确保 OpenAI API 有足够的额度
- 确保SMTP服务器配置正确，测试邮件发送：`python3 test_email.py`
- 如果邮件发送失败，检查SMTP服务器地址、端口和认证信息
- 数据库文件 `papers.db` 会自动创建
- 已抓取的论文不会重复处理，已缓存的总结不会重复调用 API
- 生产环境建议使用TLS（端口587）或SSL（端口465）加密连接

## 文件说明

- `research_agent.py`: 主程序（命令行版本）
- `web_ui.py`: Web UI 服务器
- `templates/index.html`: Web UI 前端页面
- `keywords.txt`: 关键词配置文件
- `papers.db`: SQLite 数据库（自动创建）
- `requirements.txt`: Python 依赖
- `start_web_ui.sh`: Web UI 启动脚本
- `run_scheduler.sh`: 定时任务启动脚本
- `test_email.py`: 邮件测试脚本
- `test_fetch.py`: 论文抓取测试脚本
