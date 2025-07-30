#!/bin/bash

# CSCFlow Backend 開發環境與服務器啟動腳本

# 使用說明:
#   ./backend.sh [--with-scheduler]
#   --with-scheduler: 啟用流量收集排程

set -e

echo "🚀 啟動 CSCFlow Backend 開發服務器..."

# 啟用虛擬環境
if [[ -f "../.venv/bin/activate" ]]; then
    source "../.venv/bin/activate"
fi

# 設定 PYTHONPATH 為專案根目錄
export PYTHONPATH=$(cd .. && pwd)
echo "🐍 PYTHONPATH: $PYTHONPATH"

# 檢查是否啟用流量收集排程
ENABLE_SCHEDULER="off"
if [[ "$1" == "--with-scheduler" ]]; then
    ENABLE_SCHEDULER="on"
fi

if $ENABLE_SCHEDULER; then
    echo "✅ 啟用流量收集排程"
fi

echo "✅ 啟動服務器在 http://localhost:8000"
echo "✅ API 文檔: http://localhost:8000/docs"
echo "✅ 按 Ctrl+C 停止服務器"
echo ""

# 啟動服務器
exec uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 --lifespan $ENABLE_SCHEDULER
