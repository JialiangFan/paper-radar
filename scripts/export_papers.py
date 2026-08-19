#!/usr/bin/env python3
"""把 papers 数据库中的论文导出为 data/papers/<id>.json（每篇一个文件）。

已存在的文件一律跳过（不覆盖人工整理的字段），只写新论文。
每日定时任务和一次性迁移共用此脚本。

用法: python3 scripts/export_papers.py --db papers.dev.db [--source auto]
"""

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = REPO_ROOT / "data" / "papers"

ARXIV_ID_RE = re.compile(r"(\d{4}\.\d{4,5})")


def paper_id(raw_id: str, title: str) -> str:
    """从 URL/ID 提取 arXiv 编号（去版本号）；提不出就用标题 slug。"""
    m = ARXIV_ID_RE.search(raw_id or "")
    if m:
        return m.group(1)
    slug = re.sub(r"[^a-z0-9]+", "-", (title or "untitled").lower()).strip("-")
    return slug[:80]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--source", default="auto")
    args = ap.parse_args()

    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT id, title, url, abstract, authors, date, summary, keyword, created_at FROM papers"
    ).fetchall()

    written = 0
    for r in rows:
        pid = paper_id(r["id"], r["title"])
        path = PAPERS_DIR / f"{pid}.json"
        if path.exists():
            continue
        record = {
            "id": pid,
            "title": r["title"],
            "authors": r["authors"],
            "date": r["date"],
            "year": int(r["date"][:4]) if r["date"] else None,
            "url": r["url"],
            "abstract": r["abstract"],
            "summary": r["summary"],
            "keyword": r["keyword"],
            "source": args.source,
            "created_at": r["created_at"],
        }
        path.write_text(json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")
        written += 1

    print(f"✅ 新导出 {written} 篇（共 {len(rows)} 行，跳过已存在 {len(rows) - written} 篇内含重复）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
