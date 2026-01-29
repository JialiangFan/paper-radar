#!/usr/bin/env python3
"""Send test news email using Mailgun API"""

import os
import sys
from pathlib import Path

# Load .env file if exists
try:
    from dotenv import load_dotenv
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        load_dotenv(dotenv_path=env_file)
    # Also try parent directory
    parent_env = Path(__file__).parent.parent / ".env"
    if parent_env.exists():
        load_dotenv(dotenv_path=parent_env, override=False)
except ImportError:
    pass

sys.path.insert(0, str(Path(__file__).parent))

from daily_news_email.email_builder import build_email
from daily_news_email.mailer import send_email_via_mailgun
from daily_news_email.config import load_config, apply_env_overrides

# Mock news articles for testing
mock_articles = [
    {
        "title": "AI Breakthrough: New Language Model Achieves Human-Level Performance",
        "description": "Researchers have developed a new AI model that demonstrates remarkable capabilities in understanding and generating human language. The model shows significant improvements in reasoning and context understanding.",
        "url": "https://example.com/ai-breakthrough",
        "source": {"name": "Tech News"},
        "publishedAt": "2025-12-15T10:00:00Z"
    },
    {
        "title": "Climate Summit Reaches Historic Agreement",
        "description": "World leaders have reached a consensus on new climate targets, marking a significant step forward in global environmental policy. The agreement includes commitments to reduce carbon emissions by 50% by 2030.",
        "url": "https://example.com/climate-summit",
        "source": {"name": "Global News"},
        "publishedAt": "2025-12-15T09:30:00Z"
    },
    {
        "title": "Space Exploration: New Mission to Mars Announced",
        "description": "NASA has announced plans for a new mission to Mars, with the goal of establishing a permanent research base on the red planet. The mission is scheduled to launch in 2027.",
        "url": "https://example.com/mars-mission",
        "source": {"name": "Science Daily"},
        "publishedAt": "2025-12-15T08:15:00Z"
    },
    {
        "title": "Technology Stocks Surge on Strong Earnings Reports",
        "description": "Major technology companies reported better-than-expected earnings, leading to a significant rally in tech stocks. Analysts predict continued growth in the sector.",
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
    
    # Load config
    cfg_obj = load_config(config_path)
    cfg = apply_env_overrides(cfg_obj.raw)
    
    # Build email
    email = build_email(
        articles=mock_articles,
        title="Daily News Digest - Test",
        max_articles=5
    )
    
    print("=" * 70)
    print("准备发送测试邮件（使用 Mailgun API）")
    print("=" * 70)
    print(f"\n主题: {email.subject}")
    print(f"\n收件人: {cfg['email']['to']}")
    print(f"发件人: {cfg['email']['from']}")
    print("\n邮件内容预览:")
    print("-" * 70)
    print(email.body[:500] + "..." if len(email.body) > 500 else email.body)
    print("-" * 70)
    
    # Get Mailgun credentials from environment
    mailgun_key = os.getenv("MAILGUN_API_KEY")
    mailgun_domain = os.getenv("MAILGUN_DOMAIN", "mg.zhatgpt.com")
    
    if not mailgun_key:
        print("\n❌ 错误: 未设置 MAILGUN_API_KEY 环境变量")
        print("\n请设置 Mailgun API 密钥:")
        print("  export MAILGUN_API_KEY='your-api-key'")
        print("  export MAILGUN_DOMAIN='mg.zhatgpt.com'")
        print("\n或者创建 .env 文件:")
        print("  USE_MAILGUN_API=true")
        print("  MAILGUN_API_KEY=your-api-key")
        print("  MAILGUN_DOMAIN=mg.zhatgpt.com")
        return 1
    
    print(f"\n使用 Mailgun API 发送...")
    print(f"  Domain: {mailgun_domain}")
    print(f"  API Key: {'已设置' if mailgun_key else '未设置'}")
    
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
        print("  2. 检查 MAILGUN_DOMAIN 是否正确（例如: mg.zhatgpt.com）")
        print("  3. 确认域名在 Mailgun 中已验证")
        return 1

if __name__ == "__main__":
    sys.exit(main())
