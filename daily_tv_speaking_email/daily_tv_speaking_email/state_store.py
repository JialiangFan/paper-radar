from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


@dataclass
class StateStore:
    path: Path
    data: dict[str, Any]

    @classmethod
    def load(cls, path: Path) -> "StateStore":
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                if not isinstance(data, dict):
                    data = {}
            except Exception:
                data = {}
        else:
            data = {}
        data.setdefault("snippets", [])
        data.setdefault("last_show_index", -1)
        return cls(path=path, data=data)

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=2, sort_keys=True), encoding="utf-8")

    def prune(self, keep_days: int = 30, now: datetime | None = None) -> None:
        if now is None:
            now = datetime.now(timezone.utc)
        cutoff = now - timedelta(days=keep_days)
        pruned = []
        for item in self.data.get("snippets", []):
            try:
                sent_at = datetime.fromisoformat(item.get("sent_at"))
                if sent_at.tzinfo is None:
                    sent_at = sent_at.replace(tzinfo=timezone.utc)
            except Exception:
                continue
            if sent_at >= cutoff:
                pruned.append(item)
        self.data["snippets"] = pruned

    def seen_recently(self, snippet_hash: str, keep_days: int = 30, now: datetime | None = None) -> bool:
        if now is None:
            now = datetime.now(timezone.utc)
        cutoff = now - timedelta(days=keep_days)
        for item in self.data.get("snippets", []):
            if item.get("hash") != snippet_hash:
                continue
            try:
                sent_at = datetime.fromisoformat(item.get("sent_at"))
                if sent_at.tzinfo is None:
                    sent_at = sent_at.replace(tzinfo=timezone.utc)
            except Exception:
                continue
            if sent_at >= cutoff:
                return True
        return False

    def add_snippet(self, snippet_hash: str, now: datetime | None = None, meta: dict[str, Any] | None = None) -> None:
        if now is None:
            now = datetime.now(timezone.utc)
        entry: dict[str, Any] = {"hash": snippet_hash, "sent_at": now.isoformat()}
        if meta:
            entry.update(meta)
        self.data.setdefault("snippets", []).append(entry)

    def next_show_index(self, show_count: int) -> int:
        if show_count <= 0:
            return 0
        last = int(self.data.get("last_show_index", -1) or -1)
        nxt = (last + 1) % show_count
        self.data["last_show_index"] = nxt
        return nxt
