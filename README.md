# CSCFlow System

## 專案概述

CSCFlow 是一個專為運動中心設計的人流監控與分析系統，提供以下功能：

- 收集並顯示各運動中心的即時人流數據
- 提供健身房和游泳池等區域的使用趨勢分析
- 支援多種時間範圍的數據統計（日、週、月）
- 使用者認證與授權機制

## 技術堆疊

- **後端框架**：FastAPI
- **資料庫**：PostgreSQL (透過 SQLAlchemy 和 Asyncpg)
- **快取**：Redis
- **任務排程**：APScheduler
- **容器化**：Docker 與 Docker Compose
- **前端框架**：React
- **測試框架**：Pytest 與 React Testing Library
- **持續整合/部署**：GitHub Actions

## 開發環境設置

### 使用 uv 管理依賴

1. 安裝 uv（如果尚未安裝）：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

1. 創建虛擬環境並安裝依賴：

```bash
uv venv
source .venv/bin/activate  # macOS/Linux
# 或 .venv\Scripts\activate  # Windows
uv pip install -e "."
```

### 運行開發服務器

後端服務器：

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

前端開發環境：

```bash
npm install
npm start
```

### 代碼格式化

後端代碼：

```bash
black src/
isort src/
```

前端代碼：

```bash
npm run format
```

### 運行測試

後端測試：

```bash
pytest
```

前端測試：

```bash
npm test
```

## 使用 Docker Compose

專案可以使用 Docker Compose 進行容器化部署：

```bash
docker-compose up -d
```

這將啟動以下服務：

- 前端服務（端口 3000）
- 後端 API 服務（端口 8000）
- PostgreSQL 資料庫（端口 5432）
- Redis 快取（端口 6379）

## API 文檔

啟動服務器後，可以在以下地址查看 API 文檔：

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

## 後端架構

後端架構基於 FastAPI，並包含以下模組：

- **API 模組**：提供 RESTful API 和 WebSocket 支援。
- **資料收集器**：包括 API 客戶端和網頁爬取器，用於收集運動中心的即時數據。
- **資料庫**：使用 SQLAlchemy 和 Asyncpg 與 PostgreSQL 進行交互。
- **服務層**：包含認證服務和數據流服務。
- **排程器**：使用 APScheduler 進行任務排程。

這些模組共同構成了 CSCFlow 的後端架構，支持運動中心人流管理的核心功能。

## 前端架構

前端基於 React，並包含以下模組：

- **開發工具**：使用 Vite 作為開發工具，提供快速的開發和構建體驗。
- **樣式設計**：使用 Tailwind CSS 進行樣式設計，支持自定義主題擴展。
- **代理配置**：配置了 API 和 WebSocket 代理，方便與後端進行交互。
- **測試工具**：使用 Vitest 進行單元測試，確保代碼質量。

這些模組共同構成了 CSCFlow 的前端架構，支持運動中心人流管理的核心功能。
