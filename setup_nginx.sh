#!/bin/bash
# Nginx SSL 配置脚本

set -e

echo "=========================================="
echo "Research Agent Nginx SSL 配置脚本"
echo "=========================================="

# 检查是否以 root 运行
if [ "$EUID" -ne 0 ]; then 
    echo "请使用 sudo 运行此脚本"
    exit 1
fi

# 检查 nginx 是否安装
if ! command -v nginx &> /dev/null; then
    echo "Nginx 未安装，正在安装..."
    apt update
    apt install -y nginx
fi

# 检查 certbot 是否安装
if ! command -v certbot &> /dev/null; then
    echo "Certbot 未安装，正在安装..."
    apt update
    apt install -y certbot python3-certbot-nginx
fi

# 获取域名
read -p "请输入你的域名 (例如: example.com): " DOMAIN

if [ -z "$DOMAIN" ]; then
    echo "错误: 域名不能为空"
    exit 1
fi

# 复制配置文件
CONFIG_FILE="/etc/nginx/sites-available/research_agent"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "正在创建 nginx 配置文件..."
cp "$SCRIPT_DIR/nginx_research_agent.conf" "$CONFIG_FILE"

# 替换域名
sed -i "s/your-domain.com/$DOMAIN/g" "$CONFIG_FILE"

# 检查是否已有 SSL 证书
if [ -d "/etc/letsencrypt/live/$DOMAIN" ]; then
    echo "检测到现有 SSL 证书，使用现有证书配置..."
    sed -i "s|/etc/letsencrypt/live/your-domain.com|/etc/letsencrypt/live/$DOMAIN|g" "$CONFIG_FILE"
else
    echo "未检测到 SSL 证书，将使用 Certbot 获取..."
    echo "注意: 你需要先运行以下命令获取证书:"
    echo "  sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN"
    echo ""
    echo "或者如果你想先配置 nginx 再获取证书，请确保:"
    echo "1. 域名 DNS 已正确指向此服务器"
    echo "2. 80 和 443 端口已开放"
    echo "3. 然后运行上面的 certbot 命令"
fi

# 创建符号链接
if [ -L "/etc/nginx/sites-enabled/research_agent" ]; then
    echo "配置已存在，跳过创建符号链接"
else
    ln -s "$CONFIG_FILE" /etc/nginx/sites-enabled/research_agent
    echo "已创建符号链接"
fi

# 测试配置
echo "正在测试 nginx 配置..."
if nginx -t; then
    echo "✓ Nginx 配置测试通过"
else
    echo "✗ Nginx 配置测试失败，请检查配置文件"
    exit 1
fi

# 检查防火墙
echo ""
echo "检查防火墙配置..."
if command -v ufw &> /dev/null; then
    if ufw status | grep -q "80/tcp\|443/tcp"; then
        echo "✓ 防火墙端口已配置"
    else
        echo "警告: 防火墙可能未开放 80 和 443 端口"
        read -p "是否现在开放这些端口? (y/n): " OPEN_FIREWALL
        if [ "$OPEN_FIREWALL" = "y" ]; then
            ufw allow 80/tcp
            ufw allow 443/tcp
            echo "✓ 已开放端口"
        fi
    fi
fi

echo ""
echo "=========================================="
echo "配置完成！"
echo "=========================================="
echo ""
echo "下一步:"
echo "1. 如果还没有 SSL 证书，运行:"
echo "   sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN"
echo ""
echo "2. 确保 Research Agent Web UI 正在运行:"
echo "   cd $SCRIPT_DIR"
echo "   ./start_web_ui.sh"
echo ""
echo "3. 重新加载 nginx:"
echo "   sudo systemctl reload nginx"
echo ""
echo "4. 访问 https://$DOMAIN 测试"
echo ""
