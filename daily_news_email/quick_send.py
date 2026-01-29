#!/usr/bin/env python3
"""Quick send test email - reads Mailgun config from environment or .env file"""

import os
import sys
from pathlib import Path

# Load .env if exists - check multiple locations
try:
    from dotenv import load_dotenv
    # 1. Current directory .env
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        load_dotenv(dotenv_path=env_file, override=False)
    # 2. Parent directory .env (main project .env)
    parent_env = Path(__file__).parent.parent / ".env"
    if parent_env.exists():
        load_dotenv(dotenv_path=parent_env, override=False)
    # 3. Home directory .env
    home_env = Path.home() / ".env"
    if home_env.exists():
        load_dotenv(dotenv_path=home_env, override=False)
    # 4. System-wide .env
    system_env = Path("/home/ubuntu/research_agent/.env")
    if system_env.exists():
        load_dotenv(dotenv_path=system_env, override=False)
except ImportError:
    pass

sys.path.insert(0, str(Path(__file__).parent))

from daily_news_email.email_builder import build_email
from daily_news_email.mailer import send_email_via_mailgun
from daily_news_email.config import load_config, apply_env_overrides

mock_articles = [
    {
        "title": "AI Breakthrough: New Language Model Achieves Human-Level Performance",
        "description": "Researchers have developed a new AI model that demonstrates remarkable capabilities in understanding and generating human language.",
        "url": "https://example.com/ai-breakthrough",
        "source": {"name": "Tech News"},
        "publishedAt": "2025-12-15T10:00:00Z"
    },
    {
        "title": "Climate Summit Reaches Historic Agreement",
        "description": "World leaders have reached a consensus on new climate targets, marking a significant step forward in global environmental policy.",
        "url": "https://example.com/climate-summit",
        "source": {"name": "Global News"},
        "publishedAt": "2025-12-15T09:30:00Z"
    },
    {
        "title": "Space Exploration: New Mission to Mars Announced",
        "description": "NASA has announced plans for a new mission to Mars, with the goal of establishing a permanent research base on the red planet.",
        "url": "https://example.com/mars-mission",
        "source": {"name": "Science Daily"},
        "publishedAt": "2025-12-15T08:15:00Z"
    },
    {
        "title": "Technology Stocks Surge on Strong Earnings Reports",
        "description": "Major technology companies reported better-than-expected earnings, leading to a significant rally in tech stocks.",
        "url": "https://example.com/tech-stocks",
        "source": {"name": "Financial Times"},
        "publishedAt": "2025-12-15T07:45:00Z"
    },
    {
        "title": "Medical Breakthrough: New Treatment Shows Promise for Cancer Patients",
        "description": "Clinical trials have shown promising results for a new cancer treatment, offering hope to patients with previously untreatable forms of the disease.",
        "url": "https://example.com/cancer-treatment",
        "source": {"name": "Medical Journal"},
        "publishedAt": "2025-12-15T06:20:00Z"
    }
]

def main():
    config_path = "config.yaml"
    cfg_obj = load_config(config_path)
    cfg = apply_env_overrides(cfg_obj.raw)
    
    # Build email
    email = build_email(
        articles=mock_articles,
        title="Daily News Digest - Test",
        max_articles=5
    )
    
    print("=" * 70)
    print("每日新闻邮件测试 - 使用 Mailgun API")
    print("=" * 70)
    
    # Get Mailgun credentials from environment
    mailgun_key = os.getenv("MAILGUN_API_KEY")
    mailgun_domain = os.getenv("MAILGUN_DOMAIN", "mg.zhatgpt.com")
    
    if not mailgun_key:
        print("\n❌ 错误: 未找到 MAILGUN_API_KEY")
        print("\n请通过以下方式之一设置:")
        print("\n1. 设置环境变量:")
        print("   export MAILGUN_API_KEY='your-api-key'")
        print("   export MAILGUN_DOMAIN='mg.zhatgpt.com'")
        print("\n2. 创建 .env 文件:")
        print("   cd /home/ubuntu/research_agent/daily_news_email")
        print("   echo 'MAILGUN_API_KEY=your-api-key' >> .env")
        print("   echo 'MAILGUN_DOMAIN=mg.zhatgpt.com' >> .env")
        print("\n3. 运行交互式配置:")
        print("   python3 configure_and_send.py")
        return 1
    
    print(f"\n配置信息:")
    print(f"  Domain: {mailgun_domain}")
    print(f"  API Key: {'已设置 (' + mailgun_key[:10] + '...)' if mailgun_key else '未设置'}")
    print(f"  收件人: {cfg['email']['to']}")
    print(f"  发件人: {cfg['email']['from']}")
    
    print(f"\n邮件主题: {email.subject}")
    print(f"\n正在发送邮件...")
    
    from_addr = cfg["email"]["from"]
    to_addrs = cfg["email"]["to"]
    if isinstance(to_addrs, str):
        to_addrs = [to_addrs]
    
    try:
        send_email_via_mailgun(
            mailgun_api_key=mailgun_key,
            mailgun_domain=mailgun_domain,
            from_addr=str(from_addr),
            to_addrs=[str(t) for t in to_addrs],
            subject=email.subject,
            body=email.body,
        )
        print("\n✅ 邮件发送成功！")
        print(f"   请检查收件箱: {', '.join(to_addrs)}")
        print("   （如果没收到，请检查垃圾邮件文件夹）")
        return 0
    except Exception as e:
        print(f"\n❌ 邮件发送失败: {e}")
        print("\n故障排除:")
        print("  1. 检查 MAILGUN_API_KEY 是否正确")
        print("  2. 检查 MAILGUN_DOMAIN 是否正确")
        print("  3. 确认域名在 Mailgun 中已验证")
        print("  4. 检查账户是否有足够的发送配额")
        return 1

if __name__ == "__main__":
    sys.exit(main())
