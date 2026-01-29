from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class EmailContent:
    subject: str
    body: str


def format_article(article: dict[str, Any], index: int) -> str:
    """Format a single article for email"""
    title = article.get("title", "No title")
    description = article.get("description", "")
    url = article.get("url", "")
    source = article.get("source", {}).get("name", "Unknown")
    published_at = article.get("publishedAt", "")
    
    # Format date
    date_str = ""
    if published_at:
        try:
            dt = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
            date_str = dt.strftime("%Y-%m-%d %H:%M")
        except Exception:
            date_str = published_at[:10] if len(published_at) >= 10 else ""
    
    lines = [
        f"{index}. {title}",
        f"   Source: {source}",
    ]
    
    if date_str:
        lines.append(f"   Date: {date_str}")
    
    if description:
        # Truncate description if too long
        desc = description.strip()
        if len(desc) > 200:
            desc = desc[:197] + "..."
        lines.append(f"   {desc}")
    
    if url:
        lines.append(f"   Link: {url}")
    
    return "\n".join(lines)


def build_email(
    *,
    articles: list[dict[str, Any]],
    title: str = "Daily News Digest",
    max_articles: int = 10,
) -> EmailContent:
    """Build email content from articles"""
    if not articles:
        return EmailContent(
            subject=f"{title} - No News Available",
            body="No news articles were found for today.",
        )
    
    # Limit articles
    articles_to_include = articles[:max_articles]
    
    # Build subject with date
    today = datetime.now().strftime("%Y-%m-%d")
    subject = f"{title} - {today}"
    
    # Build body
    body_lines = [
        f"{title}",
        f"Date: {today}",
        f"Total articles: {len(articles_to_include)}",
        "",
        "=" * 60,
        "",
    ]
    
    for idx, article in enumerate(articles_to_include, start=1):
        body_lines.append(format_article(article, idx))
        body_lines.append("")
    
    body_lines.append("=" * 60)
    body_lines.append("")
    body_lines.append("Powered by NewsAPI.org")
    
    body = "\n".join(body_lines)
    
    return EmailContent(subject=subject, body=body)
