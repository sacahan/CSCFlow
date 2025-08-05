# Stage 1: Build Frontend
# 使用 Node.js 18 的輕量版作為基礎映像，建立前端編譯環境
FROM node:18-alpine AS frontend-builder

# 設定工作目錄為 /app
WORKDIR /app

# 複製前端的 package.json 和 yarn.lock 以安裝依賴
COPY src/frontend/package.json ./
COPY src/frontend/yarn.lock ./

# 安裝前端依賴，並確保使用鎖定的版本
RUN yarn install --frozen-lockfile

# 複製前端所有檔案並執行編譯
COPY src/frontend ./
RUN yarn build

# Stage 2: Build Backend
# 使用 Python 3.12 的輕量版作為基礎映像，建立後端編譯環境
FROM python:3.12-slim AS backend-builder

# 設定工作目錄為 /app
WORKDIR /app

# 複製後端所有檔案，使用 .dockerignore 避免不必要的檔案
COPY . .

# Stage 3: Production
# 使用 Python 3.12 的輕量版作為基礎映像，建立生產環境
FROM python:3.12-slim

# 設定工作目錄為 /app
WORKDIR /app

# 安裝 gcc 和 python3-dev，以便編譯 C 擴展
RUN apt-get update && apt-get install -y gcc python3-dev && rm -rf /var/lib/apt/lists/*

# 設置時區為 Asia/Taipei
RUN apt-get update && apt-get install -y tzdata && \
    ln -sf /usr/share/zoneinfo/Asia/Taipei /etc/localtime && \
    echo "Asia/Taipei" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata

# 複製 pyproject.toml 並生成 requirements.txt
COPY --from=backend-builder /app/pyproject.toml /app/pyproject.toml

# 使用 pip-tools 生成 requirements.txt 並安裝依賴
RUN pip install pip-tools && pip-compile pyproject.toml && pip install -r requirements.txt

# 安裝 PostgreSQL 客戶端
RUN apt-get update && apt-get install -y postgresql-client

# 複製後端編譯後的虛擬環境及相關檔案
COPY --from=backend-builder /app/src /app/src

# 複製前端編譯後的成品至生產環境
COPY --from=frontend-builder /app/dist /app/src/frontend/dist

# 禁用 Python 輸出緩衝
ENV PYTHONUNBUFFERED=1

# 開放 8000 端口供外部訪問
EXPOSE 8000

# 使用 uvicorn 啟動後端應用，監聽所有網絡接口的 8000 端口
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
