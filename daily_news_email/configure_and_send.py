#!/usr/bin/env python3
"""Interactive script to configure Mailgun and send test email"""

import os
import sys
from pathlib import Path

# Load .env if exists
try:
    from dotenv import load_dotenv
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        load_dotenv(dotenv_path=env_file)
    parent_env = Path(__file__).parent.parent / ".env"
    if parent_env.exists():
        load_dotenv(dotenv_path=parent_env, override=False)
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
    
    print("=" * 70)
    print("每日新闻邮件测试 - 使用 Mailgun API")
    print("=" * 70)
    
    # Get Mailgun credentials
    mailgun_key = os.getenv("MAILGUN_API_KEY")
    mailgun_domain = os.getenv("MAILGUN_DOMAIN", "mg.zhatgpt.com")
    
    # If not set, try to get from user input
    if not mailgun_key:
        print("\n⚠️  Mailgun API Key 未配置")
        print("\n要使用 Mailgun 发送邮件，你需要：")
        print("1. 登录 https://app.mailgun.com/")
        print("2. 进入 Settings → API Keys")
        print("3. 复制 Private API key")
        print("\n请输入 Mailgun API Key (或按 Ctrl+C 取消):")
        mailgun_key = input("MAILGUN_API_KEY: ").strip()
        
        if not mailgun_key:
            print("\n❌ 未输入 API Key，取消发送")
            return 1
        
        # Ask for domain if not set
        if not os.getenv("MAILGUN_DOMAIN"):
            print(f"\n请输入 Mailgun Domain (默认: mg.zhatgpt.com):")
            domain_input = input("MAILGUN_DOMAIN: ").strip()
            if domain_input:
                mailgun_domain = domain_input
    
    print(f"\n配置信息:")
    print(f"  Domain: {mailgun_domain}")
    print(f"  API Key: {'已设置 (' + mailgun_key[:10] + '...)' if mailgun_key else '未设置'}")
    print(f"  收件人: {cfg['email']['to']}")
    print(f"  发件人: {cfg['email']['from']}")
    
    print(f"\n邮件主题: {email.subject}")
    print(f"\n邮件内容预览:")
    print("-" * 70)
    preview = email.body[:300] + "..." if len(email.body) > 300 else email.body
    print(preview)
    print("-" * 70)
    
    confirm = input("\n确认发送邮件? (y/n): ").strip().lower()
    if confirm != 'y':
        print("取消发送")
        return 0
    
    from_addr = cfg["email"]["from"]
    to_addrs = cfg["email"]["to"]
    if isinstance(to_addrs, str):
        to_addrs = [to_addrs]
    
    print("\n正在发送...")
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
        
        # Save to .env file
        env_file = Path(__file__).parent / ".env"
        try:
            with open(env_file, 'w') as f:
                f.write(f"USE_MAILGUN_API=true\n")
                f.write(f"MAILGUN_API_KEY={mailgun_key}\n")
                f.write(f"MAILGUN_DOMAIN={mailgun_domain}\n")
            os.chmod(env_file, 0o600)
            print(f"\n💾 配置已保存到: {env_file}")
        except Exception as e:
            print(f"\n⚠️  无法保存配置到文件: {e}")
        
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
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n取消操作")
        sys.exit(1)
