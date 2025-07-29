from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from ...db import Base


class RealTimeFlow(Base):
    """即時人流資料表"""

    __tablename__ = "real_time_flows"

    id = Column(String, primary_key=True)
    center_id = Column(String, ForeignKey("sport_centers.id"), nullable=False)
    area_type = Column(String, nullable=False)  # 區域類型（例如：游泳池、健身房等）
    current_count = Column(Integer, nullable=False)  # 目前人數
    max_count = Column(Integer, nullable=False)  # 最大容納人數
    timestamp = Column(DateTime, nullable=False, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
