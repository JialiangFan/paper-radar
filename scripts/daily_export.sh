#!/usr/bin/env bash
# 每日抓取完成后由 systemd ExecStartPost 调用：
# 把数据库里的新论文导出为 data/papers/*.json，有新增才 commit + push。
set -euo pipefail
cd "$(dirname "$0")/.."

git pull --rebase --quiet

for db in papers.db papers.dev.db; do
  [ -f "$db" ] && python3 scripts/export_papers.py --db "$db"
done

git add data/papers
if ! git diff --cached --quiet; then
  git commit -q -m "data: daily paper export $(date -u +%F)"
  git push -q
  echo "✅ 已推送新论文到 GitHub"
else
  echo "ℹ️ 无新论文，无需推送"
fi
