#!/usr/bin/env python3
"""Test script to send email using Mailgun API"""

import os
import sys
from pathlib import Path

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
        max_articles=3
    )
    
    print("=" * 60)
    print("EMAIL PREVIEW")
    print("=" * 60)
    print(f"\nSubject: {email.subject}\n")
    print(email.body)
    print("\n" + "=" * 60)
    
    # Try Mailgun if API key is provided
    mailgun_key = os.getenv("MAILGUN_API_KEY")
    mailgun_domain = os.getenv("MAILGUN_DOMAIN", "mg.zhatgpt.com")
    
    if mailgun_key:
        print(f"\n尝试使用 Mailgun API 发送...")
        print(f"Domain: {mailgun_domain}")
        
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
            print("✅ 邮件通过 Mailgun API 发送成功！")
            return 0
        except Exception as e:
            print(f"❌ Mailgun API 发送失败: {e}")
            return 1
    else:
        print("\n⚠️  未设置 MAILGUN_API_KEY 环境变量")
        print("要使用 Mailgun API 发送，请设置：")
        print("  export MAILGUN_API_KEY='your-api-key'")
        print("  export MAILGUN_DOMAIN='mg.zhatgpt.com'")
        print("\n然后运行：")
        print(f"  MAILGUN_API_KEY=your-key MAILGUN_DOMAIN=mg.zhatgpt.com python3 {sys.argv[0]}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
