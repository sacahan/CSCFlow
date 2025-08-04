# Stage 1: Build Frontend
# 使用 Node.js 18 的輕量版作為基礎映像，建立前端編譯環境
FROM node:18-alpine as frontend-builder

# 設定工作目錄為 /app
WORKDIR /app

# 複製前端的 package.json 和 yarn.lock 以安裝依賴
COPY frontend/package.json ./
COPY frontend/yarn.lock ./

# 安裝前端依賴，並確保使用鎖定的版本
RUN yarn install --frozen-lockfile

# 複製前端所有檔案並執行編譯
COPY frontend ./
RUN yarn build

# Stage 2: Build Backend
# 使用 Python 3.11 的輕量版作為基礎映像，建立後端編譯環境
FROM python:3.11-slim as backend-builder

# 設定工作目錄為 /app
WORKDIR /app

# 安裝 gcc 和 python3-dev，以便編譯 C 擴展
RUN apt-get update && apt-get install -y gcc python3-dev

# 安裝 uv 工具，用於建立虛擬環境
RUN pip install uv

# 複製 pyproject.toml 以設定 Python 專案
COPY pyproject.toml ./

# 使用 uv 建立虛擬環境並安裝專案依賴
RUN uv venv && uv pip install -e "."

# 複製後端所有檔案
COPY . .

# Stage 3: Production
# 使用 Python 3.11 的輕量版作為基礎映像，建立生產環境
FROM python:3.11-slim

# 設定工作目錄為 /app
WORKDIR /app

# 安裝 uv 工具，用於管理虛擬環境
RUN pip install uv

# 複製後端編譯後的虛擬環境及相關檔案
COPY --from=backend-builder /app/.venv /app/.venv
COPY --from=backend-builder /app/src /app/src
COPY --from=backend-builder /app/pyproject.toml /app/pyproject.toml

# 複製前端編譯後的成品至生產環境
COPY --from=frontend-builder /app/dist /app/frontend/dist

# 設定 PATH 確保使用虛擬環境中的 Python
ENV PATH="/app/.venv/bin:$PATH"

# 禁用 Python 輸出緩衝
ENV PYTHONUNBUFFERED=1

# 開放 8000 端口供外部訪問
EXPOSE 8000

# 使用 uvicorn 啟動後端應用，監聽所有網絡接口的 8000 端口
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
