from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    CheckConstraint,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from .base import Base


class RealTimeFlow(Base):
    """即時人流資料表"""

    __tablename__ = "real_time_flows"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    zip_code = Column(String(3), nullable=False)  # 運動中心郵遞區號
    area_type = Column(String(5), nullable=False)  # 'gym' 或 'pool'
    current_count = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        # 檢查 area_type 只能是 'gym' 或 'pool'
        CheckConstraint(area_type.in_(["gym", "pool"]), name="check_area_type_flow"),
        # 對郵遞區號建立索引
        Index("idx_real_time_flows_zip_timestamp", "zip_code", "timestamp"),
    )
