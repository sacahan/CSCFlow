#!/bin/bash

# 開發環境啟動腳本

set -e

echo "🚀 啟動 CSCFlow Backend 開發環境..."

# 檢查是否已安裝 uv
if ! command -v uv &> /dev/null; then
    echo "❌ uv 未安裝，請先安裝 uv"
    echo "運行: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# 創建虛擬環境（如果不存在）
if [ ! -d ".venv" ]; then
    echo "📦 創建虛擬環境..."
    uv venv
fi

# 安裝依賴
echo "📚 安裝依賴..."
uv pip install -e ".[dev]"

echo "✅ 開發環境設置完成！"
echo ""
echo "現在您可以運行以下命令："
echo "  ./start-dev.sh                                             # 啟動開發服務器"
echo "  .venv/bin/pytest                                           # 運行測試"
echo "  .venv/bin/black src/                                       # 格式化代碼"
echo "  .venv/bin/isort src/                                       # 整理導入"
