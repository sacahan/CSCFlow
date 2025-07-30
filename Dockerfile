# Stage 1: Build
FROM python:3.11-slim as builder

WORKDIR /app

# 安裝 uv
RUN pip install uv

COPY pyproject.toml ./
RUN uv venv && uv pip install -e "."

COPY . .

# Stage 2: Production
FROM python:3.11-slim

WORKDIR /app

# 安裝 uv
RUN pip install uv

# 複製項目檔案和虛擬環境
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src
COPY --from=builder /app/pyproject.toml /app/pyproject.toml

# 確保使用虛擬環境
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
