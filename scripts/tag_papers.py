#!/usr/bin/env python3
"""用 claude -p 给 data/papers/ 里没有 topics 字段的论文打主题标签（写回 JSON）。

标签只能取自 data/taxonomy.json 的 slug，每篇 1-3 个。幂等、可中断续跑。

用法: python3 scripts/tag_papers.py [--limit 100] [--batch-size 40] [--model haiku]
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = REPO_ROOT / "data" / "papers"
TAXONOMY = json.loads((REPO_ROOT / "data" / "taxonomy.json").read_text(encoding="utf-8"))

PROMPT_HEADER = """你是论文主题分类器。给下面每篇论文标注 1-3 个主题标签，标签只能从这个 taxonomy 里选 slug：

{taxonomy}

规则：
- 选最贴合的 1-3 个，宁缺毋滥；确实都不贴合才用 other
- 只输出一个 JSON 对象，格式 {{"<论文ID>": ["slug", ...], ...}}，不要输出任何其他文字

论文列表：
{papers}"""


def load_untagged():
    out = []
    for f in sorted(PAPERS_DIR.glob("*.json")):
        p = json.loads(f.read_text(encoding="utf-8"))
        if not p.get("topics"):
            out.append((f, p))
    return out


def tag_batch(batch, model):
    tax_lines = "\n".join(f"- {slug}: {v['name']} — {v['desc']}" for slug, v in TAXONOMY.items())
    paper_lines = "\n\n".join(
        f"[{p['id']}] {p['title']}\n{(p.get('abstract') or p.get('summary') or '')[:500]}"
        for _, p in batch)
    prompt = PROMPT_HEADER.format(taxonomy=tax_lines, papers=paper_lines)

    r = subprocess.run(["claude", "-p", "--model", model], input=prompt,
                       capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        raise RuntimeError(f"claude -p 失败: {r.stderr[:300]}")
    raw = r.stdout[r.stdout.find("{"): r.stdout.rfind("}") + 1]
    result = json.loads(raw)

    written = 0
    for f, p in batch:
        topics = [t for t in result.get(p["id"], []) if t in TAXONOMY]
        if not topics:
            continue
        p["topics"] = topics
        f.write_text(json.dumps(p, ensure_ascii=False, indent=1), encoding="utf-8")
        written += 1
    return written


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--batch-size", type=int, default=40)
    ap.add_argument("--model", default="haiku")
    args = ap.parse_args()

    todo = load_untagged()[: args.limit]
    print(f"待打标: {len(todo)} 篇")
    done = 0
    for i in range(0, len(todo), args.batch_size):
        batch = todo[i: i + args.batch_size]
        done += tag_batch(batch, args.model)
        print(f"  进度 {min(i + args.batch_size, len(todo))}/{len(todo)}（已写回 {done}）")
    print(f"✅ 完成，共写回 {done} 篇")
    return 0


if __name__ == "__main__":
    sys.exit(main())
