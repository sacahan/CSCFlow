#!/bin/zsh

# =================================================================
# 資料庫遷移管理工具
# =================================================================
#
# 此腳本用於管理資料庫遷移操作，支援以下功能：
# 1. 建立新的遷移檔案
# 2. 執行遷移
# 3. 回滾遷移
# 4. 重置資料庫
# 5. 查看遷移狀態
# 6. 查看遷移歷史
#
# 使用方式：
# -----------------------------------------------------------------
# 1. 賦予執行權限：
#    chmod +x scripts/migrate.sh
#
# 2. 基本命令：
#    ./migrate.sh [命令] [參數]
#
# 可用命令：
# -----------------------------------------------------------------
# create [描述]  : 建立新的遷移檔案
# up             : 執行所有未完成的遷移
# down [步驟]    : 回滾指定步數的遷移
# reset          : 重置資料庫（回滾所有遷移後重新執行）
# status         : 顯示目前的遷移狀態
# history        : 顯示遷移歷史
# help           : 顯示使用說明
#
# 注意事項：
# -----------------------------------------------------------------
# 1. 執行 reset 命令時會清空資料庫，請謹慎使用
# 2. 建議在執行遷移前先備份資料庫
# 3. 確保已安裝 alembic 套件
# 4. 遷移描述盡量具體，方便追蹤變更
#
# =================================================================

# 顯示使用說明
showHelp() {
    echo "資料庫遷移管理工具"
    echo
    echo "用法:"
    echo "  ./migrate.sh [命令] [參數]"
    echo
    echo "可用命令:"
    echo "  create [描述]   - 建立新的遷移"
    echo "  up             - 執行所有未完成的遷移"
    echo "  down [步驟]     - 回滾指定步數的遷移（預設: 1）"
    echo "  reset          - 回滾所有遷移然後重新執行"
    echo "  status         - 顯示目前的遷移狀態"
    echo "  history        - 顯示遷移歷史"
    echo
    echo "範例:"
    echo "  ./migrate.sh create '新增使用者表格'"
    echo "  ./migrate.sh up"
    echo "  ./migrate.sh down 2"
    echo "  ./migrate.sh status"
}

# 啟用虛擬環境
activateVirtualEnv() {
    if [[ -f "../../.venv/bin/activate" ]]; then
        source "../../.venv/bin/activate"
    else
        echo "錯誤: 請先建立虛擬環境"
        exit 1
    fi
}

# 檢查必要的工具是否安裝
checkRequirements() {
    if ! command -v alembic &> /dev/null; then
        echo "錯誤: 需要安裝 alembic"
        echo "請執行: pip install alembic"
        exit 1
    fi
}

# 建立新的遷移
createMigration() {
    if [[ -z "$1" ]]; then
        echo "錯誤: 請提供遷移的描述"
        echo "範例: ./migrate.sh create '新增使用者表格'"
        exit 1
    fi
    alembic revision --autogenerate -m "$1"
}

# 執行遷移
runUpgrade() {
    alembic upgrade head
}

# 回滾遷移
runDowngrade() {
    local steps=${1:-1}
    alembic downgrade -${steps}
}

# 重置資料庫
resetDatabase() {
    echo "警告: 這將會重置整個資料庫。是否繼續？ [y/N]"
    read confirm
    if [[ $confirm =~ ^[Yy]$ ]]; then
        alembic downgrade base
        alembic upgrade head
        echo "資料庫已重置"
    else
        echo "操作已取消"
    fi
}

# 顯示遷移狀態
showStatus() {
    alembic current
    alembic history --verbose
}

# 顯示遷移歷史
showHistory() {
    alembic history --verbose
}

# 主程式
main() {
    activateVirtualEnv # 啟用虛擬環境
    checkRequirements # 檢查必要工具

    case "$1" in
        create)
            createMigration "$2"
            ;;
        up)
            runUpgrade
            ;;
        down)
            runDowngrade "$2"
            ;;
        reset)
            resetDatabase
            ;;
        status)
            showStatus
            ;;
        history)
            showHistory
            ;;
        help|--help|-h|"")
            showHelp
            ;;
        *)
            echo "錯誤: 未知的命令 '$1'"
            echo "使用 './migrate.sh help' 查看可用命令"
            exit 1
            ;;
    esac
}

# 執行主程式
main "$@"
