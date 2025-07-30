from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from .api.routes import api_router
from .schedulers.flow_task import FlowTask

from contextlib import asynccontextmanager

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="CSCFlow API")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊 API 路由
app.include_router(api_router)

# 建立 FlowTask 實例
flow_task = FlowTask()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager for startup and shutdown events.
    Initializes and shuts down FlowTask.
    """
    try:
        logger.info("正在啟動流量收集排程...")
        await flow_task.start()
        logger.info("流量收集排程已成功啟動")
        yield
    except Exception as e:
        logger.error(f"啟動流量收集排程時發生錯誤: {str(e)}")
        raise
    finally:
        try:
            logger.info("正在關閉流量收集排程...")
            await flow_task.shutdown()
            logger.info("流量收集排程已成功關閉")
        except Exception as e:
            logger.error(f"關閉流量收集排程時發生錯誤: {str(e)}")


app.router.lifespan_context = lifespan


@app.get("/")
async def root():
    return {"message": "Welcome to CSCFlow API"}
