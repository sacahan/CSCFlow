import unittest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from src.models import Base
from src.db import get_db, SessionLocal


class TestDatabase(unittest.TestCase):
    def setUp(self):
        """設置測試環境"""
        self.test_database_url = "sqlite:///:memory:"
        self.engine = create_engine(self.test_database_url)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self.session = self.SessionLocal()
        Base.metadata.create_all(bind=self.engine)

    def tearDown(self):
        """清理測試環境"""
        self.session.close()
        Base.metadata.drop_all(bind=self.engine)

    def test_get_db(self):
        """測試資料庫連接取得"""
        db = next(get_db())
        self.assertIsNotNone(db)
        db.close()

    def test_database_tables(self):
        """測試資料庫表格是否正確創建"""
        inspector = inspect(self.engine)
        tables = inspector.get_table_names()

        # 檢查是否創建了所需的表格
        self.assertIn("sport_centers", tables)
        self.assertIn("real_time_flows", tables)

        # 檢查表格的列
        sport_center_columns = {
            col["name"] for col in inspector.get_columns("sport_centers")
        }
        self.assertIn("id", sport_center_columns)
        self.assertIn("name", sport_center_columns)
        self.assertIn("address", sport_center_columns)
        self.assertIn("website_url", sport_center_columns)  # 新增檢查 website_url 列

        flow_columns = {col["name"] for col in inspector.get_columns("real_time_flows")}
        self.assertIn("id", flow_columns)
        self.assertIn("center_id", flow_columns)
        self.assertIn("current_count", flow_columns)

    def test_session_creation(self):
        """測試 Session 創建"""
        session = SessionLocal()
        self.assertIsNotNone(session)
        session.close()


if __name__ == "__main__":
    unittest.main()
