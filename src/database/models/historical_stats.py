"""
歷史統計記錄模型
"""

from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Date,
    DateTime,
    CheckConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from .base import Base


class HistoricalStats(Base):
    """歷史統計記錄表"""

    __tablename__ = "historical_stats"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    zip_code = Column(String(3), nullable=False)  # 運動中心郵遞區號
    area_type = Column(String(5), nullable=False)
    avg_count = Column(Float, nullable=False)
    max_count = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        # 檢查 area_type 只能是 'gym' 或 'pool'
        CheckConstraint(area_type.in_(["gym", "pool"]), name="check_area_type_stats"),
    )
