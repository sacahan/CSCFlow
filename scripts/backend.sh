#!/bin/bash

# CSCFlow Backend 開發環境與服務器啟動腳本

# 獲取專案根目錄的絕對路徑
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." &> /dev/null && pwd )"

set -e

echo "🚀 啟動 CSCFlow Backend 開發服務器..."

# 啟用虛擬環境
if [[ -f "${PROJECT_ROOT}/.venv/bin/activate" ]]; then
    source "${PROJECT_ROOT}/.venv/bin/activate"
fi

# 設定 PYTHONPATH 為專案根目錄
export PYTHONPATH=$(cd .. && pwd)
echo "🐍 PYTHONPATH: $PYTHONPATH"

echo "✅ 啟動服務器在 http://localhost:8000"
echo "✅ API 文檔: http://localhost:8000/docs"
echo "✅ 按 Ctrl+C 停止服務器"
echo ""

# 啟動服務器
exec uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
