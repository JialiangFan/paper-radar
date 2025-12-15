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


def _coalesce(*vals):
    for v in vals:
        if v is not None:
            return v
    return None


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
    data.setdefault("language", "en")
    data.setdefault("snippet_duration_sec", 45)
    data.setdefault("timezone", "America/Indiana/Indianapolis")

    return Config(raw=data, path=p)


def apply_env_overrides(cfg: dict[str, Any]) -> dict[str, Any]:
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

    cfg = dict(cfg)
    cfg["email"] = email

    # Optional overrides
    if os.getenv("DTVSE_STATE_PATH"):
        cfg["state_path"] = os.getenv("DTVSE_STATE_PATH")

    if os.getenv("DTVSE_SHOW_SELECTION"):
        cfg["show_selection"] = os.getenv("DTVSE_SHOW_SELECTION")

    return cfg
