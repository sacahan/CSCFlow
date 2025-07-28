import unittest
from datetime import datetime, timezone
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import SportCenter, RealTimeFlow, HistoricalStats, Base


class TestModels(unittest.TestCase):
    def setUp(self):
        self.test_database_url = "sqlite:///:memory:"
        self.engine = create_engine(self.test_database_url)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        Base.metadata.create_all(bind=self.engine)
        self.session = self.SessionLocal()

    def tearDown(self):
        self.session.close()

    def test_sport_center_model(self):
        """測試 SportCenter 模型"""
        now = datetime.utcnow()
        center = SportCenter(
            name="運動中心A",
            address="地址A",
            location={"lat": 25.033, "lng": 121.565},
            max_capacity={"gym": 100, "pool": 50},
            website_url="https://example.com",  # 新增 website_url 屬性
            created_at=now,
            updated_at=now,
        )
        self.session.add(center)
        self.session.commit()

        result = self.session.query(SportCenter).filter_by(name="運動中心A").first()
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "運動中心A")
        self.assertEqual(
            result.created_at.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d")
        )
        self.assertEqual(
            result.website_url, "https://example.com"
        )  # 新增檢查 website_url 屬性

    def test_real_time_flow_model(self):
        """測試 RealTimeFlow 模型"""
        test_uuid = uuid.uuid4()
        now = datetime.utcnow()
        flow = RealTimeFlow(
            center_id=test_uuid,
            area_type="gym",
            current_count=10,
            timestamp=now,
        )
        self.session.add(flow)
        self.session.commit()

        result = self.session.query(RealTimeFlow).filter_by(area_type="gym").first()
        self.assertIsNotNone(result)
        self.assertEqual(result.current_count, 10)
        self.assertEqual(
            result.timestamp.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d")
        )

    def test_historical_stats_model(self):
        """測試 HistoricalStats 模型"""
        test_uuid = uuid.uuid4()
        now = datetime.now(timezone.utc)  # 使用正確的 UTC 時區表示
        stats = HistoricalStats(
            center_id=test_uuid,
            area_type="gym",
            avg_count=20.5,
            max_count=30,
            date=now.date(),
            created_at=now,
            updated_at=now,
        )
        self.session.add(stats)
        self.session.commit()

        result = self.session.query(HistoricalStats).filter_by(area_type="gym").first()
        self.assertIsNotNone(result)
        self.assertEqual(str(result.center_id), str(test_uuid))
        self.assertEqual(result.area_type, "gym")
        self.assertEqual(result.avg_count, 20.5)
        self.assertEqual(result.max_count, 30)
        self.assertEqual(result.date, now.date())
        self.assertEqual(
            result.created_at.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d")
        )
        self.assertEqual(
            result.updated_at.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d")
        )


if __name__ == "__main__":
    unittest.main()
