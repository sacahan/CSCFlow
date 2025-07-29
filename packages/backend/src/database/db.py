from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# 載入 .env 檔案
load_dotenv()

# 從環境變數取得資料庫連線 URL
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL and not DATABASE_URL.startswith("postgresql+asyncpg://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# 建立非同步資料庫引擎
engine = create_async_engine(DATABASE_URL)

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
