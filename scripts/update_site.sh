#!/usr/bin/env bash
# droplet 上每 30 分钟由 cron 调用：拉取最新数据 → 构建静态站 → 同步到 nginx 目录。
set -euo pipefail
cd "$(dirname "$0")/.."

git pull --rebase --autostash --quiet
python3 scripts/build_site.py > /dev/null
rsync -a --delete site/ /var/www/paper-radar/
