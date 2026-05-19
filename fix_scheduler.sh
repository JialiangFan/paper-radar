#!/usr/bin/env bash
# 修复 research-agent-scheduler.service：补上 LD_PRELOAD 让 sqlite3 能在 python3.13 下加载。
# 用 systemd drop-in，不动主 unit 文件。需要 sudo。
#
# 用法：
#   bash fix_scheduler.sh
# 或：
#   chmod +x fix_scheduler.sh && ./fix_scheduler.sh

set -euo pipefail

UNIT=research-agent-scheduler.service
DROPIN_DIR=/etc/systemd/system/${UNIT}.d
DROPIN_FILE=${DROPIN_DIR}/override.conf
LIBSQLITE=/home/ubuntu/miniconda3/lib/libsqlite3.so.3.51.0

echo "==> 1) 检查依赖文件存在"
if [[ ! -f "$LIBSQLITE" ]]; then
    echo "❌ 找不到 $LIBSQLITE — 请确认 miniconda 路径"
    exit 1
fi
echo "    OK: $LIBSQLITE"

echo "==> 2) 创建 drop-in 目录"
sudo mkdir -p "$DROPIN_DIR"

echo "==> 3) 写入 override.conf"
sudo tee "$DROPIN_FILE" > /dev/null <<EOF
[Service]
Environment="LD_PRELOAD=${LIBSQLITE}"
EOF
echo "    写入内容："
sudo cat "$DROPIN_FILE" | sed 's/^/      /'

echo "==> 4) systemctl daemon-reload"
sudo systemctl daemon-reload

echo "==> 5) 手动触发一次 scheduler 验证"
sudo systemctl start "$UNIT"

echo "==> 6) 等待 oneshot 完成（最多 5 分钟）"
for i in $(seq 1 60); do
    state=$(systemctl is-active "$UNIT" || true)
    if [[ "$state" != "activating" ]]; then
        break
    fi
    sleep 5
done

echo "==> 7) 服务状态"
sudo systemctl status "$UNIT" --no-pager | head -15

echo ""
echo "==> 8) 最近 40 条 journal"
sudo journalctl -u "$UNIT" -n 40 --no-pager

echo ""
echo "==> 9) 判定"
last_result=$(systemctl show "$UNIT" -p Result --value)
exit_code=$(systemctl show "$UNIT" -p ExecMainStatus --value)
if [[ "$last_result" == "success" && "$exit_code" == "0" ]]; then
    echo "✅ 修复成功 (Result=$last_result, ExecMainStatus=$exit_code)"
    echo "   下次自动触发时间："
    systemctl list-timers research-agent-scheduler.timer --no-pager | head -3
    exit 0
else
    echo "❌ 仍然失败 (Result=$last_result, ExecMainStatus=$exit_code)"
    echo "   请把上面 journal 输出贴回给 Claude 继续排查"
    exit 1
fi
