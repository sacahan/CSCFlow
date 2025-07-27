#!/bin/bash

# 啟動 CSCFlow Backend 開發服務器腳本

set -e

echo "🚀 啟動 CSCFlow Backend 開發服務器..."

# 檢查是否在正確的目錄
if [ ! -f "pyproject.toml" ]; then
    echo "❌ 請在 backend 目錄中運行此腳本"
    exit 1
fi

# 檢查虛擬環境是否存在
if [ ! -d ".venv" ]; then
    echo "❌ 虛擬環境不存在，請先運行 ./setup-dev.sh"
    exit 1
fi

echo "✅ 啟動服務器在 http://localhost:8000"
echo "✅ API 文檔: http://localhost:8000/docs"
echo "✅ 按 Ctrl+C 停止服務器"
echo ""

# 使用完整路徑啟動服務器
exec .venv/bin/uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
