#!/usr/bin/env python3
"""Test script to send a sample news email"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from daily_news_email.email_builder import build_email
from daily_news_email.mailer import send_email
from daily_news_email.config import load_config, apply_env_overrides

# Mock news articles for testing
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
    
    # Load config
    cfg_obj = load_config(config_path)
    cfg = apply_env_overrides(cfg_obj.raw)
    
    # Build email with mock data
    email = build_email(
        articles=mock_articles,
        title="Daily News Digest - Test",
        max_articles=5
    )
    
    print("=" * 60)
    print("EMAIL PREVIEW (DRY RUN)")
    print("=" * 60)
    print(f"\nSubject: {email.subject}\n")
    print(email.body)
    print("\n" + "=" * 60)
    
    # Ask if user wants to send
    if len(sys.argv) > 1 and sys.argv[1] == "--send":
        print("\nSending email...")
        
        from_addr = cfg["email"]["from"]
        to_addrs = cfg["email"]["to"]
        if isinstance(to_addrs, str):
            to_addrs = [to_addrs]
        
        smtp_host = cfg.get("email", {}).get("smtp_host")
        smtp_port = cfg.get("email", {}).get("smtp_port")
        smtp_user = cfg.get("email", {}).get("smtp_user")
        smtp_password = cfg.get("email", {}).get("smtp_password")
        
        try:
            send_email(
                smtp_host=str(smtp_host) if smtp_host else None,
                smtp_port=int(smtp_port) if smtp_port is not None else None,
                smtp_user=str(smtp_user) if smtp_user else None,
                smtp_password=str(smtp_password) if smtp_password else None,
                from_addr=str(from_addr),
                to_addrs=[str(t) for t in to_addrs],
                subject=email.subject,
                body=email.body,
                debug=True,
            )
            print("✅ Email sent successfully!")
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return 1
    else:
        print("\nTo actually send the email, run:")
        print(f"  python3 {sys.argv[0]} --send")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
