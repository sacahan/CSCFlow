#!/bin/bash

# CSCFlow 排程器獨立執行腳本

# 顯示使用說明
show_usage() {
    echo "使用方法: $0 [選項]"
    echo "選項:"
    echo "排程模式:"
    echo "  run              啟動所有定時排程作業 (預設)"
    echo "  flow             僅啟動流量收集排程"
    echo "  trend            僅啟動趨勢統計排程"
    echo "一次性執行:"
    echo "  once             執行所有排程作業一次"
    echo "  once-f           僅執行流量收集一次"
    echo "  once-t           僅執行趨勢統計一次"
    echo "其他:"
    echo "  help             顯示此說明"
    exit 1
}

# 獲取專案根目錄的絕對路徑
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." &> /dev/null && pwd )"

# 解析命令列參數
MODE=${1:-run}

case $MODE in
    run)
        echo "🚀 啟動所有 CSCFlow 定時排程作業..."
        ;;
    flow)
        echo "🚀 啟動流量收集排程..."
        ;;
    trend)
        echo "🚀 啟動趨勢統計排程..."
        ;;
    once)
        echo "🔍 執行所有排程作業一次..."
        ;;
    once-f)
        echo "🔍 執行一次流量收集..."
        ;;
    once-t)
        echo "🔍 執行一次趨勢統計..."
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        echo "❌ 無效的選項: $MODE"
        show_usage
        ;;
esac

# 啟用虛擬環境
if [[ -f "${PROJECT_ROOT}/.venv/bin/activate" ]]; then
    source "${PROJECT_ROOT}/.venv/bin/activate"
fi

# 設定 PYTHONPATH 為專案根目錄
export PYTHONPATH="${PROJECT_ROOT}"
echo "🐍 PYTHONPATH: $PYTHONPATH"

if [ "$MODE" = "run" ]; then
    echo "✅ 排程器將每 5 分鐘執行一次流量收集  (8-20 點)"
    echo "✅ 每小時執行一次趨勢統計 (9-21 點)"
    echo "✅ 每天晚上 10 點執行日統計"
elif [ "$MODE" = "flow" ]; then
    echo "✅ 排程器將每 5 分鐘執行一次流量收集 (8-20 點)"
elif [ "$MODE" = "trend" ]; then
    echo "✅ 每小時執行一次趨勢統計 (9-21 點)"
    echo "✅ 每天晚上 10 點執行日統計"
elif [ "$MODE" = "once" ]; then
    echo "✅ 將立即執行一次流量收集和趨勢統計"
elif [ "$MODE" = "once-f" ]; then
    echo "✅ 將立即執行一次流量收集"
elif [ "$MODE" = "once-t" ]; then
    echo "✅ 將立即執行一次趨勢統計"
fi

echo "✅ 日誌將寫入到 scheduler.log 檔案"
echo "✅ 按 Ctrl+C 停止程式"
echo ""

# 切換到專案根目錄
cd "${PROJECT_ROOT}"
PYTHONPATH="${PROJECT_ROOT}"

# 啟動排程器
python3 -c "
import asyncio
from src.schedulers.run_scheduler import main
asyncio.run(main('$MODE'))
"
