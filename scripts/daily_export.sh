#!/usr/bin/env bash
# 每日抓取完成后由 systemd ExecStartPost 调用：
# 把数据库里的新论文导出为 data/papers/*.json，有新增才 commit + push。
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="$HOME/.local/bin:$PATH"   # droplet 的 claude CLI 在这里，cron 环境不带

git pull --rebase --autostash --quiet

for db in papers.db papers.dev.db; do
  [ -f "$db" ] && python3 scripts/export_papers.py --db "$db"
done

# 给新论文打主题标签（失败不阻塞导出，漏掉的下次续跑）
python3 scripts/tag_papers.py || echo "⚠️ 打标失败，跳过"

git add data/papers
if ! git diff --cached --quiet; then
  git commit -q -m "data: daily paper export $(date -u +%F)"
  git push -q
  echo "✅ 已推送新论文到 GitHub"
else
  echo "ℹ️ 无新论文，无需推送"
fi
