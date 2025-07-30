#!/bin/bash

# CSCFlow 排程器獨立執行腳本

set -e

# 獲取專案根目錄的絕對路徑
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." &> /dev/null && pwd )"

echo "🚀 啟動 CSCFlow 排程器..."

# 啟用虛擬環境
if [[ -f "${PROJECT_ROOT}/.venv/bin/activate" ]]; then
    source "${PROJECT_ROOT}/.venv/bin/activate"
fi

# 設定 PYTHONPATH 為專案根目錄
export PYTHONPATH="${PROJECT_ROOT}"
echo "🐍 PYTHONPATH: $PYTHONPATH"

echo "✅ 排程器將每 5 分鐘執行一次流量收集"
echo "✅ 日誌將寫入到 scheduler.log 檔案"
echo "✅ 按 Ctrl+C 停止排程器"
echo ""

# 啟動排程器
cd "${PROJECT_ROOT}"  # 切換到專案根目錄
exec python -m src.schedulers.run_scheduler
