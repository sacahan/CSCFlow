#!/bin/zsh

# 確保腳本在錯誤時停止執行
set -e

# 獲取專案根目錄的絕對路徑
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." &> /dev/null && pwd )"

# 檢查 Docker 是否安裝
if ! command -v docker &> /dev/null
then
    echo "Docker 未安裝，請先安裝 Docker。"
    exit 1
fi

# 檢查參數
if [[ $# -lt 1 ]]; then
    echo "未提供選項，將執行所有容器的 build 建置 (建議使用: $0 build all)"
    ACTION="build"
fi

ACTION=${ACTION:-$1}
TARGET=$2
MODE=$3

# 預設要支援的平台
# PLATFORMS="linux/amd64,linux/arm64"
PLATFORMS="linux/amd64"
# 若要推到 Docker Hub，預設的使用者帳號
DOCKERHUB_USER="sacahan"


# 根據 service 名稱取得對應的 Dockerfile
get_dockerfile_for_service() {
    svc="$1"
    if [[ "$svc" == "task" ]]; then
        echo "$PROJECT_ROOT/Dockerfile.task"
        return
    fi
    if [[ "$svc" == "flow" ]]; then
        echo "$PROJECT_ROOT/Dockerfile"
        return
    fi
    if [[ -f "$PROJECT_ROOT/Dockerfile.$svc" ]]; then
        echo "$PROJECT_ROOT/Dockerfile.$svc"
        return
    fi
    if [[ -f "$PROJECT_ROOT/Dockerfile" ]]; then
        echo "$PROJECT_ROOT/Dockerfile"
        return
    fi
    return 1
}


# 執行指定操作
case $ACTION in
    help)
        echo "使用方式: $0 <help|build|deploy|all> <task|flow|all>"
        echo "選項:"
        echo "  help       顯示此幫助訊息"
        echo "  build      建置本地平台映像檔（只支援本機架構，無 buildx），可指定 task、flow 或 all"
        echo "             本地映像僅支援目前主機平台（如 linux/arm64），不支援多平台。"
        echo "  deploy     建置並推送多平台映像檔到 Docker Hub（使用 buildx），可指定 task、flow 或 all"
        echo "             deploy 會建置 linux/amd64, linux/arm64 並推送到 Docker Hub，無本地 image。"
        exit 0
    ;;
    build)
        # build: 只建置本地平台映像，不使用 buildx，不支援多平台
        if [[ -z "$TARGET" || "$TARGET" == "all" ]]; then
            targets=("task" "flow")
        else
            targets=("$TARGET")
        fi
        for svc in "${targets[@]}"; do
            DOCKERFILE_PATH=$(get_dockerfile_for_service "$svc") || { echo "找不到 Dockerfile for $svc"; exit 1; }
            IMAGE_TAG="${DOCKERHUB_USER}/cscflow-${svc}:latest"
            echo "建置本地映像: image=$IMAGE_TAG, dockerfile=$DOCKERFILE_PATH"
            # 只建置本地平台映像
            docker build -t "$IMAGE_TAG" -f "$DOCKERFILE_PATH" "$PROJECT_ROOT"
        done
    ;;
    deploy)
        # deploy: 建置多平台映像並推送到 Docker Hub（不保留本地 image）
        if [[ -z "$TARGET" || "$TARGET" == "all" ]]; then
            targets=("task" "flow")
        else
            targets=("$TARGET")
        fi
        BUILDER_NAME="multiarch-builder"
        if ! docker buildx inspect "$BUILDER_NAME" &> /dev/null; then
            echo "建立 buildx builder: $BUILDER_NAME"
            docker buildx create --name "$BUILDER_NAME" --driver docker-container --use
        else
            echo "使用已存在的 buildx builder: $BUILDER_NAME"
            docker buildx use "$BUILDER_NAME"
        fi
        docker buildx inspect --bootstrap
        echo "註冊 QEMU multiarch binfmt 支援 (需要 Docker 允許 --privileged) ..."
        docker run --rm --privileged tonistiigi/binfmt:latest --install all || \
        docker run --rm --privileged multiarch/qemu-user-static --reset -p yes || true
        for svc in "${targets[@]}"; do
            DOCKERFILE_PATH=$(get_dockerfile_for_service "$svc") || { echo "找不到 Dockerfile for $svc"; exit 1; }
            IMAGE_TAG="${DOCKERHUB_USER}/cscflow-${svc}:latest"
            echo "建置並推送多平台映像: image=$IMAGE_TAG, dockerfile=$DOCKERFILE_PATH"
            # buildx --push 只推送，不保留本地 image
            docker buildx build --platform "$PLATFORMS" --push -t "$IMAGE_TAG" -f "$DOCKERFILE_PATH" "$PROJECT_ROOT"
        done
    ;;
    *)
        echo "未知操作: $ACTION"
        echo "使用方式: $0 <help|build|deploy|all> <task|flow|all>"
        exit 1
    ;;
esac

echo "$ACTION $TARGET 完成！"
