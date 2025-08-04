#!/bin/zsh

# 確保腳本在錯誤時停止執行
set -e

# 定義變數
DOCKER_COMPOSE_FILE="docker-compose.yml"
DOCKER_COMPOSE_SCRIPT_FILE="scripts/docker-compose.yml"

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

# 建置 Scheduler 容器
echo "正在建置 Scheduler 容器..."
docker-compose -f $DOCKER_COMPOSE_FILE build scheduler

# 建置 Flow 容器
echo "正在建置 Flow 容器..."
docker-compose -f $DOCKER_COMPOSE_FILE build flow

# 啟動所有服務
echo "正在啟動所有服務..."
docker-compose -f $DOCKER_COMPOSE_FILE up -d

# 確認服務狀態
echo "服務狀態："
docker-compose -f $DOCKER_COMPOSE_FILE ps

# 啟動腳本中的 Redis 和 Postgres
echo "正在啟動 Redis 和 Postgres..."
docker-compose -f $DOCKER_COMPOSE_SCRIPT_FILE up -d

# 確認腳本中的服務狀態
echo "腳本中的服務狀態："
docker-compose -f $DOCKER_COMPOSE_SCRIPT_FILE ps

echo "建置與部署完成！"
