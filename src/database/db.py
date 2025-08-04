from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# 載入 .env 檔案
load_dotenv()

# 從環境變數取得資料庫連線 URL
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_POOL_SIZE = os.getenv("DATABASE_POOL_SIZE", 20)
DATABASE_MAX_OVERFLOW = os.getenv("DATABASE_MAX_OVERFLOW", 10)
DATABASE_POOL_TIMEOUT = os.getenv("DATABASE_POOL_TIMEOUT", 60)
DATABASE_POOL_RECYCLE = os.getenv("DATABASE_POOL_RECYCLE", 3600)


# 建立非同步資料庫引擎
engine = create_async_engine(
    url=DATABASE_URL,
    pool_size=int(DATABASE_POOL_SIZE),
    max_overflow=int(DATABASE_MAX_OVERFLOW),
    pool_timeout=int(DATABASE_POOL_TIMEOUT),
    pool_recycle=int(DATABASE_POOL_RECYCLE),
)

# 建立非同步 Session
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# 提供資料庫相依注入
async def get_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
