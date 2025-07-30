#!/bin/bash

# CSCFlow Backend 開發環境與服務器啟動腳本

set -e

echo "🚀 啟動 CSCFlow Backend 開發服務器..."

# 啟用虛擬環境
if [[ -f ".venv/bin/activate" ]]; then
    source ".venv/bin/activate"
fi

echo "✅ 啟動服務器在 http://localhost:8000"
echo "✅ API 文檔: http://localhost:8000/docs"
echo "✅ 按 Ctrl+C 停止服務器"
echo ""

# 啟動服務器
exec uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
