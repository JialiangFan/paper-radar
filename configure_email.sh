#!/bin/bash
# Research Agent 邮件配置脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"

echo "=========================================="
echo "Research Agent 邮件配置工具"
echo "=========================================="
echo ""

# 检查 .env 文件是否存在
if [ ! -f "$ENV_FILE" ]; then
    echo "创建新的 .env 文件..."
    touch "$ENV_FILE"
fi

# 读取当前配置
if [ -f "$ENV_FILE" ]; then
    CURRENT_SENDER=$(grep "^EMAIL_SENDER=" "$ENV_FILE" | cut -d'=' -f2 | tr -d '"' | tr -d "'")
    CURRENT_PASSWORD=$(grep "^EMAIL_PASSWORD=" "$ENV_FILE" | cut -d'=' -f2 | tr -d '"' | tr -d "'")
    CURRENT_RECEIVER=$(grep "^EMAIL_RECEIVER=" "$ENV_FILE" | cut -d'=' -f2 | tr -d '"' | tr -d "'")
    CURRENT_SMTP_SERVER=$(grep "^SMTP_SERVER=" "$ENV_FILE" | cut -d'=' -f2 | tr -d '"' | tr -d "'")
    CURRENT_SMTP_PORT=$(grep "^SMTP_PORT=" "$ENV_FILE" | cut -d'=' -f2 | tr -d '"' | tr -d "'")
    CURRENT_SMTP_USE_SSL=$(grep "^SMTP_USE_SSL=" "$ENV_FILE" | cut -d'=' -f2 | tr -d '"' | tr -d "'")
    CURRENT_SMTP_USE_TLS=$(grep "^SMTP_USE_TLS=" "$ENV_FILE" | cut -d'=' -f2 | tr -d '"' | tr -d "'")
fi

# 显示当前配置
echo "当前邮件配置："
echo "  发送邮箱: ${CURRENT_SENDER:-未设置}"
echo "  接收邮箱: ${CURRENT_RECEIVER:-未设置}"
echo "  SMTP服务器: ${CURRENT_SMTP_SERVER:-localhost}"
echo "  SMTP端口: ${CURRENT_SMTP_PORT:-25}"
echo "  使用SSL: ${CURRENT_SMTP_USE_SSL:-false}"
echo "  使用TLS: ${CURRENT_SMTP_USE_TLS:-true}"
echo "  密码: ${CURRENT_PASSWORD:+已设置（隐藏）}"
echo ""

# 询问是否要修改
read -p "是否要修改邮件配置? (y/n): " MODIFY
if [ "$MODIFY" != "y" ] && [ "$MODIFY" != "Y" ]; then
    echo "取消配置。"
    exit 0
fi

# 输入新的配置
echo ""
echo "请输入新的邮件配置："
read -p "发送邮箱 (例如: sender@yourdomain.com): " NEW_SENDER
read -p "SMTP服务器地址 (默认: localhost): " NEW_SMTP_SERVER
NEW_SMTP_SERVER=${NEW_SMTP_SERVER:-localhost}

read -p "SMTP端口 (默认: 25, SSL使用465, TLS使用587): " NEW_SMTP_PORT
NEW_SMTP_PORT=${NEW_SMTP_PORT:-25}

read -p "使用SSL? (y/n, 默认: n): " USE_SSL_INPUT
if [ "$USE_SSL_INPUT" = "y" ] || [ "$USE_SSL_INPUT" = "Y" ]; then
    NEW_SMTP_USE_SSL="true"
    NEW_SMTP_USE_TLS="false"
else
    NEW_SMTP_USE_SSL="false"
    read -p "使用TLS? (y/n, 默认: y): " USE_TLS_INPUT
    if [ "$USE_TLS_INPUT" = "n" ] || [ "$USE_TLS_INPUT" = "N" ]; then
        NEW_SMTP_USE_TLS="false"
    else
        NEW_SMTP_USE_TLS="true"
    fi
fi

read -p "SMTP密码 (如果服务器需要认证，留空则跳过认证): " NEW_PASSWORD
read -p "接收邮箱 (例如: recipient@example.com): " NEW_RECEIVER

# 验证输入
if [ -z "$NEW_SENDER" ] || [ -z "$NEW_RECEIVER" ]; then
    echo "错误: 发送邮箱和接收邮箱必须填写！"
    exit 1
fi

# 备份原文件
if [ -f "$ENV_FILE" ]; then
    cp "$ENV_FILE" "$ENV_FILE.backup.$(date +%Y%m%d_%H%M%S)"
fi

# 更新或添加配置
# 读取现有文件，更新或添加邮件配置
TEMP_FILE=$(mktemp)
IN_SECTION=false
EMAIL_UPDATED=false

while IFS= read -r line || [ -n "$line" ]; do
    if [[ "$line" =~ ^#.*邮件配置 ]]; then
        IN_SECTION=true
        echo "$line" >> "$TEMP_FILE"
        echo "# SMTP服务器配置" >> "$TEMP_FILE"
        echo "EMAIL_SENDER=$NEW_SENDER" >> "$TEMP_FILE"
        if [ -n "$NEW_PASSWORD" ]; then
            echo "EMAIL_PASSWORD=$NEW_PASSWORD" >> "$TEMP_FILE"
        fi
        echo "EMAIL_RECEIVER=$NEW_RECEIVER" >> "$TEMP_FILE"
        echo "SMTP_SERVER=$NEW_SMTP_SERVER" >> "$TEMP_FILE"
        echo "SMTP_PORT=$NEW_SMTP_PORT" >> "$TEMP_FILE"
        echo "SMTP_USE_SSL=$NEW_SMTP_USE_SSL" >> "$TEMP_FILE"
        echo "SMTP_USE_TLS=$NEW_SMTP_USE_TLS" >> "$TEMP_FILE"
        EMAIL_UPDATED=true
        continue
    fi
    
    if [[ "$line" =~ ^(EMAIL_(SENDER|PASSWORD|RECEIVER)|SMTP_(SERVER|PORT|USE_SSL|USE_TLS))= ]]; then
        # 跳过旧的邮件配置行
        continue
    fi
    
    echo "$line" >> "$TEMP_FILE"
done < "$ENV_FILE"

# 如果没有找到邮件配置部分，添加到最后
if [ "$EMAIL_UPDATED" = false ]; then
    echo "" >> "$TEMP_FILE"
    echo "# 邮件配置 - SMTP服务器" >> "$TEMP_FILE"
    echo "EMAIL_SENDER=$NEW_SENDER" >> "$TEMP_FILE"
    if [ -n "$NEW_PASSWORD" ]; then
        echo "EMAIL_PASSWORD=$NEW_PASSWORD" >> "$TEMP_FILE"
    fi
    echo "EMAIL_RECEIVER=$NEW_RECEIVER" >> "$TEMP_FILE"
    echo "SMTP_SERVER=$NEW_SMTP_SERVER" >> "$TEMP_FILE"
    echo "SMTP_PORT=$NEW_SMTP_PORT" >> "$TEMP_FILE"
    echo "SMTP_USE_SSL=$NEW_SMTP_USE_SSL" >> "$TEMP_FILE"
    echo "SMTP_USE_TLS=$NEW_SMTP_USE_TLS" >> "$TEMP_FILE"
fi

mv "$TEMP_FILE" "$ENV_FILE"

echo ""
echo "✅ 邮件配置已更新！"
echo ""
echo "新配置："
echo "  发送邮箱: $NEW_SENDER"
echo "  接收邮箱: $NEW_RECEIVER"
echo "  SMTP服务器: $NEW_SMTP_SERVER"
echo "  SMTP端口: $NEW_SMTP_PORT"
echo "  使用SSL: $NEW_SMTP_USE_SSL"
echo "  使用TLS: $NEW_SMTP_USE_TLS"
if [ -n "$NEW_PASSWORD" ]; then
    echo "  密码: 已设置（隐藏）"
else
    echo "  密码: 未设置（将跳过SMTP认证）"
fi
echo ""

# 询问是否重启服务
read -p "是否重启 Web UI 服务以应用新配置? (y/n): " RESTART
if [ "$RESTART" = "y" ] || [ "$RESTART" = "Y" ]; then
    echo "正在重启服务..."
    sudo systemctl restart research-agent-web.service
    sleep 2
    if systemctl is-active --quiet research-agent-web.service; then
        echo "✅ 服务已重启并运行正常"
    else
        echo "⚠️  服务重启后可能有问题，请检查: sudo systemctl status research-agent-web.service"
    fi
fi

echo ""
echo "=========================================="
echo "配置完成！"
echo "=========================================="
echo ""
echo "提示："
echo "1. 常见SMTP配置："
echo "   - 本地服务器: localhost:25 (无SSL/TLS)"
echo "   - 标准SMTP: yourdomain.com:25 (可选TLS)"
echo "   - 安全SMTP: yourdomain.com:587 (TLS) 或 :465 (SSL)"
echo ""
echo "2. 测试邮件发送："
echo "   cd $SCRIPT_DIR"
echo "   python3 test_email.py"
echo ""
