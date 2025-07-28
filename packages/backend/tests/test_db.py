import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base
from src.db import init_db, migrate_db


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.test_database_url = "sqlite:///:memory:"
        self.engine = create_engine(self.test_database_url)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        Base.metadata.create_all(bind=self.engine)

    def test_init_db(self):
        """測試資料庫初始化"""
        try:
            init_db()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"資料庫初始化失敗: {e}")

    def test_migrate_db(self):
        """測試資料庫遷移"""
        try:
            migrate_db()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"資料庫遷移失敗: {e}")


if __name__ == "__main__":
    unittest.main()
