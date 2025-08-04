from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging
from .api.routes import api_router
from pathlib import Path

# 設定日誌，方便追蹤應用程式的運行狀態
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化 FastAPI 應用，並設定應用名稱
app = FastAPI(title="CSCFlow Service", description="運動中心人流數據收集與分析服務")

# 配置 CORS 中介軟體，允許特定來源的跨域請求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或使用 ["*"] 允許所有來源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊 API 路由，將所有 API 路由集中管理
app.include_router(api_router)

# 取得專案根目錄路徑
BASE_DIR = Path(__file__).resolve().parent.parent

# 設定前端靜態檔案目錄
frontend_dist_dir = BASE_DIR / "src" / "frontend" / "dist"
app.mount(
    "/", StaticFiles(directory=str(frontend_dist_dir), html=True), name="frontend"
)


# 根路由，返回簡單的歡迎訊息
@app.get("/api")
async def root():
    return {"message": "Welcome to CSCFlow API"}
