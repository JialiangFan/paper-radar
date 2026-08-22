#!/usr/bin/env python3
"""拉取 Hugging Face Daily Papers，合并进 data/papers/。

两种情况：
- 论文已在库（按 arXiv 编号匹配）：只合并/更新 hf_upvotes 字段（社区热度信号）
- 不在库且 upvotes >= 阈值：作为新论文导入（source=hf-daily，无 topics，
  由同一 daily 流程里的 tag_papers.py 接手打标）

幂等：内容无变化不写文件。

用法: python3 scripts/fetch_hf.py [--min-upvotes 20]
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

from export_papers import paper_id

REPO_ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = REPO_ROOT / "data" / "papers"

API_URL = "https://huggingface.co/api/daily_papers"


def fetch_daily():
    r = requests.get(API_URL, timeout=30)
    r.raise_for_status()
    return r.json()


def to_record(paper: dict, pid: str, upvotes: int) -> dict:
    date = (paper.get("publishedAt") or "")[:10]
    authors = ", ".join(
        a.get("name", "") for a in paper.get("authors", []) if a.get("name")
    )
    return {
        "id": pid,
        "title": paper.get("title", "").strip(),
        "authors": authors,
        "date": date,
        "year": int(date[:4]) if date else None,
        "url": f"https://arxiv.org/abs/{pid}",
        "abstract": (paper.get("summary") or "").strip(),
        "summary": None,
        "keyword": None,
        "source": "hf-daily",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "hf_upvotes": upvotes,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-upvotes", type=int, default=20,
                    help="不在库的论文，upvotes 达到该值才导入")
    args = ap.parse_args()

    entries = fetch_daily()
    merged = imported = 0
    for entry in entries:
        paper = entry.get("paper") or entry
        raw_id = paper.get("id") or ""
        upvotes = paper.get("upvotes") or 0
        pid = paper_id(raw_id, paper.get("title") or "")
        path = PAPERS_DIR / f"{pid}.json"

        if path.exists():
            record = json.loads(path.read_text(encoding="utf-8"))
            if record.get("hf_upvotes") != upvotes:
                record["hf_upvotes"] = upvotes
                path.write_text(json.dumps(record, ensure_ascii=False, indent=1),
                                encoding="utf-8")
                merged += 1
        elif upvotes >= args.min_upvotes:
            record = to_record(paper, pid, upvotes)
            path.write_text(json.dumps(record, ensure_ascii=False, indent=1),
                            encoding="utf-8")
            imported += 1

    print(f"✅ HF daily: 共 {len(entries)} 篇，更新 upvotes {merged} 篇，"
          f"新导入 {imported} 篇（阈值 {args.min_upvotes}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
