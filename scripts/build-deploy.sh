#!/bin/zsh

# 確保腳本在錯誤時停止執行
set -e

# 獲取專案根目錄的絕對路徑
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." &> /dev/null && pwd )"

# 定義變數
DOCKER_COMPOSE_FILE="$PROJECT_ROOT/docker-compose.yml"

# 檢查 Docker 是否安裝
if ! command -v docker &> /dev/null
then
    echo "Docker 未安裝，請先安裝 Docker。"
    exit 1
fi

# 檢查 Docker Compose 是否安裝
if ! command -v docker-compose &> /dev/null
then
    echo "Docker Compose 未安裝，請先安裝 Docker Compose。"
    exit 1
fi

# 檢查參數
if [[ $# -lt 1 ]]; then
    echo "未提供選項，將執行所有容器的建置與部署..."
    ACTION="all"
fi

ACTION=${ACTION:-$1}
TARGET=$2

# 執行指定操作
case $ACTION in
    help)
        echo "使用方式: $0 <help|build|deploy|all> <task|flow>"
        echo "選項:"
        echo "  help       顯示此幫助訊息"
        echo "  build      建置指定的容器 (task 或 flow)"
        echo "  deploy     部署指定的容器 (task 或 flow)"
        echo "  all        建置並部署所有容器，或指定 task 或 flow"
        exit 0
        ;;
    build)
        echo "正在建置 $TARGET 容器..."
        docker-compose -f $DOCKER_COMPOSE_FILE build $TARGET
        ;;
    deploy)
        echo "正在停止 $TARGET 容器..."
        docker-compose -f $DOCKER_COMPOSE_FILE down $TARGET
        echo "正在部署 $TARGET 容器..."
        docker-compose -f $DOCKER_COMPOSE_FILE up -d $TARGET
        ;;
    all)
        if [[ -z $TARGET ]]; then
            echo "正在建置所有容器 (task 和 flow)..."
            docker-compose -f $DOCKER_COMPOSE_FILE build task flow
            echo "正在停止所有容器 (task 和 flow)..."
            docker-compose -f $DOCKER_COMPOSE_FILE down task flow
            echo "正在部署所有容器 (task 和 flow)..."
            docker-compose -f $DOCKER_COMPOSE_FILE up -d task flow
        else
            echo "正在建置 $TARGET 容器..."
            docker-compose -f $DOCKER_COMPOSE_FILE build $TARGET
            echo "正在停止 $TARGET 容器..."
            docker-compose -f $DOCKER_COMPOSE_FILE down $TARGET
            echo "正在部署 $TARGET 容器..."
            docker-compose -f $DOCKER_COMPOSE_FILE up -d $TARGET
        fi
        ;;
    *)
        echo "未知操作: $ACTION"
        echo "使用方式: $0 <help|build|deploy|all> <task|flow>"
        exit 1
        ;;
esac

# 確認服務狀態
echo "服務狀態："
docker-compose -f $DOCKER_COMPOSE_FILE ps

echo "$ACTION $TARGET 完成！"
