from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import Any

from newsapi import NewsApiClient


class NewsClient:
    """Client for fetching news from NewsAPI"""

    def __init__(self, api_key: str | None = None, debug: bool = False):
        self.api_key = api_key or os.getenv("NEWS_API_KEY", "")
        if not self.api_key:
            raise ValueError("NEWS_API_KEY environment variable is required")
        self.client = NewsApiClient(api_key=self.api_key)
        self.debug = debug

    def _log(self, msg: str) -> None:
        if self.debug:
            print(f"[news_client] {msg}")

    def get_top_headlines(
        self,
        country: str = "us",
        category: str | None = None,
        sources: str | None = None,
        q: str | None = None,
        page_size: int = 20,
    ) -> list[dict[str, Any]]:
        """Get top headlines"""
        try:
            self._log(f"Fetching top headlines: country={country}, category={category}")
            response = self.client.get_top_headlines(
                country=country,
                category=category,
                sources=sources,
                q=q,
                page_size=page_size,
            )
            articles = response.get("articles", [])
            self._log(f"Retrieved {len(articles)} articles")
            return articles
        except Exception as e:
            self._log(f"Error fetching headlines: {e}")
            raise

    def get_everything(
        self,
        q: str | None = None,
        sources: str | None = None,
        domains: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        language: str = "en",
        sort_by: str = "publishedAt",
        page_size: int = 20,
    ) -> list[dict[str, Any]]:
        """Get everything (all articles)"""
        try:
            self._log(f"Fetching everything: q={q}, language={language}")
            
            # Default to today's date if not specified
            if not from_date:
                from_date = datetime.now().strftime("%Y-%m-%d")
            if not to_date:
                to_date = datetime.now().strftime("%Y-%m-%d")
            
            response = self.client.get_everything(
                q=q,
                sources=sources,
                domains=domains,
                from_param=from_date,
                to=to_date,
                language=language,
                sort_by=sort_by,
                page_size=page_size,
            )
            articles = response.get("articles", [])
            self._log(f"Retrieved {len(articles)} articles")
            return articles
        except Exception as e:
            self._log(f"Error fetching everything: {e}")
            raise

    def get_sources(
        self,
        category: str | None = None,
        language: str = "en",
        country: str | None = None,
    ) -> list[dict[str, Any]]:
        """Get available news sources"""
        try:
            self._log(f"Fetching sources: category={category}, language={language}")
            response = self.client.get_sources(
                category=category,
                language=language,
                country=country,
            )
            sources = response.get("sources", [])
            self._log(f"Retrieved {len(sources)} sources")
            return sources
        except Exception as e:
            self._log(f"Error fetching sources: {e}")
            raise
