"""
歷史統計記錄模型
"""

from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    DateTime,
    CheckConstraint,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from .base import Base


class HistoricalStats(Base):
    """歷史統計記錄表：用於儲存不同時間區間（每小時、每日）的統計數據"""

    __tablename__ = "historical_stats"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    zip_code = Column(String(3), nullable=False)  # 運動中心郵遞區號
    area_type = Column(String(5), nullable=False)  # gym 或 pool
    stats_type = Column(String(10), nullable=False)  # hourly, daily

    # 統計指標
    avg_count = Column(Float, nullable=False)  # 期間平均人數
    max_count = Column(Integer, nullable=False)  # 期間最大人數
    min_count = Column(Integer, nullable=False)  # 期間最小人數

    # 統計期間
    start_date = Column(DateTime, nullable=False)  # 統計開始日期
    end_date = Column(DateTime, nullable=False)  # 統計結束日期

    # 時間戳記
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        # 檢查約束條件
        CheckConstraint(area_type.in_(["gym", "pool"]), name="check_area_type_stats"),
        CheckConstraint(stats_type.in_(["hourly", "daily"]), name="check_stats_type"),
        # 唯一性約束
        UniqueConstraint(
            "zip_code",
            "area_type",
            "stats_type",
            "start_date",
            name="unique_stats_constraint",
        ),
    )
