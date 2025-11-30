#!/bin/bash
# Research Agent Scheduler Systemd 服务配置脚本

set -e

echo "=========================================="
echo "Research Agent Scheduler Systemd 服务配置"
echo "=========================================="

# 检查是否以 root 运行
if [ "$EUID" -ne 0 ]; then 
    echo "请使用 sudo 运行此脚本"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_FILE="$SCRIPT_DIR/research-agent-scheduler.service"
SYSTEMD_FILE="/etc/systemd/system/research-agent-scheduler.service"

# 检查 conda 环境
echo "检查 conda 环境..."
CONDA_BASE="/home/ubuntu/miniconda3"

if [ ! -d "$CONDA_BASE" ]; then
    echo "错误: 未找到 conda 安装目录 $CONDA_BASE"
    exit 1
fi

# 检查 paper_agent 环境是否存在
if [ -d "$CONDA_BASE/envs/paper_agent" ]; then
    echo "✓ 找到 paper_agent conda 环境"
    USE_ENV="paper_agent"
elif [ -d "$CONDA_BASE/envs/base" ]; then
    echo "⚠ 未找到 paper_agent 环境，将使用 base 环境"
    USE_ENV="base"
else
    echo "⚠ 将使用 conda base 环境"
    USE_ENV="base"
fi

# 检查 .env 文件是否存在
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo "⚠ 警告: 未找到 .env 文件，服务可能无法正常工作"
    echo "   请确保 $SCRIPT_DIR/.env 文件存在并包含必要的配置"
fi

# 复制服务文件
echo "正在复制服务文件..."
cp "$SERVICE_FILE" "$SYSTEMD_FILE"

# 根据环境调整配置
if [ "$USE_ENV" = "paper_agent" ]; then
    # 使用 paper_agent 环境
    sed -i 's|ExecStart=.*|ExecStart=/home/ubuntu/miniconda3/bin/conda run -n paper_agent python /home/ubuntu/research_agent/research_agent.py schedule|' "$SYSTEMD_FILE"
    sed -i 's|CONDA_DEFAULT_ENV=.*|CONDA_DEFAULT_ENV=paper_agent|' "$SYSTEMD_FILE"
    sed -i 's|CONDA_PREFIX=.*|CONDA_PREFIX=/home/ubuntu/miniconda3/envs/paper_agent|' "$SYSTEMD_FILE"
    echo "✓ 配置为使用 paper_agent 环境"
else
    # 使用 base 环境
    sed -i 's|ExecStart=.*|ExecStart=/home/ubuntu/miniconda3/bin/python /home/ubuntu/research_agent/research_agent.py schedule|' "$SYSTEMD_FILE"
    sed -i 's|CONDA_DEFAULT_ENV=.*|CONDA_DEFAULT_ENV=base|' "$SYSTEMD_FILE"
    sed -i 's|CONDA_PREFIX=.*|CONDA_PREFIX=/home/ubuntu/miniconda3|' "$SYSTEMD_FILE"
    echo "✓ 配置为使用 base 环境"
fi

# 重新加载 systemd
echo "重新加载 systemd..."
systemctl daemon-reload

# 启用服务（开机自启）
echo "启用服务（开机自启）..."
systemctl enable research-agent-scheduler.service

# 询问是否立即启动服务
read -p "是否立即启动服务? (y/n): " START_NOW
if [ "$START_NOW" = "y" ] || [ "$START_NOW" = "Y" ]; then
    echo "启动服务..."
    if systemctl start research-agent-scheduler.service; then
        echo "✓ 服务启动成功"
    else
        echo "✗ 服务启动失败，查看日志:"
        journalctl -u research-agent-scheduler.service -n 20 --no-pager
        exit 1
    fi
    
    # 等待一下，检查状态
    sleep 2
    
    # 检查服务状态
    echo ""
    echo "=========================================="
    echo "服务状态:"
    echo "=========================================="
    systemctl status research-agent-scheduler.service --no-pager -l
fi

echo ""
echo "=========================================="
echo "配置完成！"
echo "=========================================="
echo ""
echo "常用命令:"
echo "  查看状态: sudo systemctl status research-agent-scheduler"
echo "  查看日志: sudo journalctl -u research-agent-scheduler -f"
echo "  重启服务: sudo systemctl restart research-agent-scheduler"
echo "  停止服务: sudo systemctl stop research-agent-scheduler"
echo "  启动服务: sudo systemctl start research-agent-scheduler"
echo ""
echo "服务已设置为开机自启"
echo "定时任务将在每天美东时间 09:00 自动运行"
echo ""
