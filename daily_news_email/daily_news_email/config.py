from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass
class Config:
    raw: dict[str, Any]
    path: Path


def load_config(path: str) -> Config:
    p = Path(path).expanduser().resolve()
    if not p.exists():
        raise FileNotFoundError(str(p))

    if p.suffix.lower() in {".yaml", ".yml"}:
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
    elif p.suffix.lower() == ".json":
        data = json.loads(p.read_text(encoding="utf-8"))
    else:
        raise ValueError("Config must be .yaml/.yml or .json")

    if not isinstance(data, dict):
        raise ValueError("Config must be a mapping/object")

    # Defaults
    data.setdefault("country", "us")
    data.setdefault("language", "en")
    data.setdefault("max_articles", 10)
    data.setdefault("category", None)
    data.setdefault("query", None)

    return Config(raw=data, path=p)


def apply_env_overrides(cfg: dict[str, Any]) -> dict[str, Any]:
    """Apply environment variable overrides"""
    cfg = dict(cfg)

    # Email overrides
    email = dict(cfg.get("email") or {})

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    email_from = os.getenv("EMAIL_FROM")
    email_to = os.getenv("EMAIL_TO")

    if smtp_host:
        email["smtp_host"] = smtp_host
    if smtp_port:
        try:
            email["smtp_port"] = int(smtp_port)
        except ValueError:
            pass
    if smtp_user:
        email["smtp_user"] = smtp_user
    if smtp_password:
        email["smtp_password"] = smtp_password
    if email_from:
        email["from"] = email_from
    if email_to:
        tos = [t.strip() for t in email_to.split(",") if t.strip()]
        if tos:
            email["to"] = tos

    cfg["email"] = email

    # News API overrides
    if os.getenv("NEWS_API_KEY"):
        cfg["news_api_key"] = os.getenv("NEWS_API_KEY")
    if os.getenv("NEWS_COUNTRY"):
        cfg["country"] = os.getenv("NEWS_COUNTRY")
    if os.getenv("NEWS_LANGUAGE"):
        cfg["language"] = os.getenv("NEWS_LANGUAGE")
    if os.getenv("NEWS_CATEGORY"):
        cfg["category"] = os.getenv("NEWS_CATEGORY")
    if os.getenv("NEWS_QUERY"):
        cfg["query"] = os.getenv("NEWS_QUERY")
    if os.getenv("NEWS_MAX_ARTICLES"):
        try:
            cfg["max_articles"] = int(os.getenv("NEWS_MAX_ARTICLES"))
        except ValueError:
            pass

    return cfg
