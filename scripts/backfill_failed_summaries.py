#!/usr/bin/env python3
"""用 Codex 重新生成数据库中的失败占位摘要。"""

import argparse
import json
import sqlite3
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import research_agent as agent


def summarize_batch(rows, max_retries=3):
    papers = [
        {"id": row["id"], "title": row["title"], "abstract": row["abstract"] or ""}
        for row in rows
    ]
    prompt = """请为下面每篇论文生成简洁中文总结。每篇必须包含：
1. **核心创新点**：一句话概括。
2. **主要方法**：简述所用技术或模型。
3. **结论/性能**：只依据摘要描述效果；未提供数字时不要编造。

只输出一个合法 JSON 对象，键为论文 id，值为 Markdown 总结，不要输出代码围栏或其他文字。

论文：
""" + json.dumps(papers, ensure_ascii=False)

    for attempt in range(max_retries):
        try:
            raw = agent._call_codex_cli(prompt)
            start, end = raw.find("{"), raw.rfind("}")
            if start < 0 or end < start:
                raise ValueError("Codex 输出中没有 JSON 对象")
            result = json.loads(raw[start:end + 1])
            missing = [row["id"] for row in rows if not result.get(row["id"])]
            if missing:
                raise ValueError(f"Codex 输出缺少 {len(missing)} 篇论文")
            return result
        except (RuntimeError, ValueError, json.JSONDecodeError) as exc:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt
            print(f"  ⚠️ 批次失败，{wait_time} 秒后重试：{exc}")
            time.sleep(wait_time)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default=agent.DB_PATH)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--batch-size", type=int, default=10)
    args = parser.parse_args()

    agent.DB_PATH = args.db
    connection = sqlite3.connect(args.db)
    connection.row_factory = sqlite3.Row
    query = """SELECT id, title, url, abstract, authors, date, keyword
               FROM papers WHERE summary = ? ORDER BY created_at ASC"""
    params = [agent.FAILED_SUMMARY]
    if args.limit is not None:
        query += " LIMIT ?"
        params.append(args.limit)
    rows = connection.execute(query, params).fetchall()
    connection.close()

    print(f"待补录: {len(rows)} 篇（数据库: {args.db}）")
    succeeded = 0
    for offset in range(0, len(rows), args.batch_size):
        batch = rows[offset:offset + args.batch_size]
        try:
            summaries = summarize_batch(batch)
            for row in batch:
                paper = dict(row)
                agent.save_paper(
                    paper, summaries[row["id"]], paper.get("keyword") or "", sent=False
                )
                succeeded += 1
        except Exception as exc:
            print(f"  ❌ 批次 {offset + 1}-{offset + len(batch)} 失败：{exc}")
        print(f"  进度 {offset + len(batch)}/{len(rows)}，成功 {succeeded}")

    print(f"完成：成功 {succeeded}，失败 {len(rows) - succeeded}")
    return 0 if succeeded == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
