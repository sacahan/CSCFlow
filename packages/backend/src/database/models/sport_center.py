"""
運動中心模型
"""

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from .base import Base


class SportCenter(Base):
    """運動中心資料表"""

    __tablename__ = "sport_centers"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    phone = Column(String)
    website = Column(String)
    collector_type = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
