from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# 載入 .env 檔案
load_dotenv()

# 從環境變數取得資料庫連線 URL
DATABASE_URL = os.getenv("DATABASE_URL")

# 建立資料庫引擎
engine = create_engine(DATABASE_URL)

# 建立 Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 提供資料庫相依注入
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
