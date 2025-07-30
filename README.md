# CSCFlow Backend

CSCFlow 後端 API 服務，基於 FastAPI 構建。

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
uv pip install -e ".[dev]"
```

### 運行開發服務器

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 代碼格式化

```bash
black src/
isort src/
```

### 運行測試

```bash
pytest
```

## API 文檔

啟動服務器後，可以在以下地址查看 API 文檔：

-   Swagger UI: <http://localhost:8000/docs>
-   ReDoc: <http://localhost:8000/redoc>
