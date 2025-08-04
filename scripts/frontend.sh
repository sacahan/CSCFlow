#!/bin/bash

# CSCFlow Frontend 開發環境與服務器啟動腳本

# 獲取專案根目錄的絕對路徑
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." &> /dev/null && pwd )"
FRONTEND_DIR="${PROJECT_ROOT}/src/frontend"

set -e

echo "🚀 啟動 CSCFlow Frontend 開發服務器..."

# 檢查 Node.js 環境
if ! command -v node &> /dev/null; then
    echo "❌ 未安裝 Node.js，請先安裝 Node.js"
    exit 1
fi

# 檢查 yarn
if ! command -v yarn &> /dev/null; then
    echo "⚙️ 未安裝 yarn，正在安裝..."
    npm install -g yarn
fi

# 切換到前端目錄
cd "$FRONTEND_DIR"

# 檢查是否需要安裝依賴
if [ ! -d "node_modules" ]; then
    echo "📦 安裝依賴套件..."
    yarn install
fi

echo "✅ 啟動開發服務器在 http://localhost:3000"
echo "✅ 按 Ctrl+C 停止服務器"
echo ""

# 啟動開發服務器
exec yarn dev
