from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
import os
import asyncio
from contextlib import asynccontextmanager
import logging

# 載入 .env 檔案
load_dotenv()

# 從環境變數取得資料庫連線 URL
DATABASE_URL = os.getenv("DATABASE_URL")

# 從環境變數取得資料庫連線池設定
DATABASE_POOL_SIZE = int(os.getenv("DATABASE_POOL_SIZE", 20))
DATABASE_MAX_OVERFLOW = int(os.getenv("DATABASE_MAX_OVERFLOW", 10))
DATABASE_POOL_TIMEOUT = int(os.getenv("DATABASE_POOL_TIMEOUT", 60))
DATABASE_POOL_RECYCLE = int(os.getenv("DATABASE_POOL_RECYCLE", 3600))
# 建立非同步資料庫引擎，優化連線池設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_async_engine(
    DATABASE_URL,
    pool_size=DATABASE_POOL_SIZE,  # 增加基礎連線池大小
    max_overflow=DATABASE_MAX_OVERFLOW,  # 增加最大溢出連線數
    pool_timeout=DATABASE_POOL_TIMEOUT,  # 增加等待超時時間
    pool_recycle=DATABASE_POOL_RECYCLE,  # 定期回收連線
    pool_pre_ping=True,  # 啟用連線健康檢查
    echo=os.getenv("DATABASE_ECHO", "false").lower() == "true",  # SQL 除錯輸出
)

# 建立非同步 Session
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# 提供資料庫相依注入，加入斷線重連機制
async def get_session():
    retries = 3
    for attempt in range(retries):
        try:
            async with AsyncSessionLocal() as session:
                yield session
        except OperationalError as e:
            if attempt < retries - 1:
                await asyncio.sleep(2**attempt)  # 指數回退重試
                continue
            else:
                raise e
        finally:
            await session.close()


@asynccontextmanager
async def get_db_session():
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()


async def check_db_health():
    try:
        async with AsyncSessionLocal() as session:
            await session.execute("SELECT 1")
            return True
    except Exception as e:
        logger.error(f"資料庫健康檢查失敗: {str(e)}")
        return False
