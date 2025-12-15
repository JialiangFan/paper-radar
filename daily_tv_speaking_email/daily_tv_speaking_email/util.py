from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


_TAG_RE = re.compile(r"<[^>]+>")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def strip_html(text: str) -> str:
    return _TAG_RE.sub("", text)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_bool_env(name: str, default: bool = False) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return v.strip().lower() in {"1", "true", "yes", "y", "on"}


def safe_json_loads(s: str):
    try:
        return json.loads(s)
    except Exception:
        return None


@dataclass(frozen=True)
class TimeRange:
    start_ms: int
    end_ms: int

    def format_range(self) -> str:
        return f"{format_srt_time(self.start_ms)}–{format_srt_time(self.end_ms)}"


def format_srt_time(ms: int) -> str:
    if ms < 0:
        ms = 0
    total_sec = ms // 1000
    hh = total_sec // 3600
    mm = (total_sec % 3600) // 60
    ss = total_sec % 60
    return f"{hh:02}:{mm:02}:{ss:02}"


def get_tz(name: str) -> ZoneInfo:
    return ZoneInfo(name)
