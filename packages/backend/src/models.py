from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Date,
    JSON,
    TIMESTAMP,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func

# 定義 SQLAlchemy 的基底類別，用於建立 ORM 模型
Base = declarative_base()


# 定義運動中心的資料表模型
class SportCenter(Base):
    __tablename__ = "sport_centers"  # 資料表名稱

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )  # 唯一識別碼，使用 UUID
    name = Column(String(100), nullable=False, unique=True)  # 運動中心名稱，必填且唯一
    address = Column(String(255), nullable=False)  # 運動中心地址，必填
    max_capacity = Column(JSON, nullable=False)  # 最大容量資訊，包含健身房與游泳池
    website_url = Column(String(255), nullable=False)  # 運動中心的官方網站 URL，必填
    created_at = Column(
        TIMESTAMP(timezone=True), default="CURRENT_TIMESTAMP"
    )  # 建立時間
    updated_at = Column(
        TIMESTAMP(timezone=True), default="CURRENT_TIMESTAMP"
    )  # 更新時間


# 定義即時流量的資料表模型
class RealTimeFlow(Base):
    __tablename__ = "real_time_flows"  # 資料表名稱

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )  # 唯一識別碼，使用 UUID
    center_id = Column(
        UUID(as_uuid=True), ForeignKey("sport_centers.id"), nullable=False
    )  # 關聯的運動中心 ID
    area_type = Column(String(20), nullable=False)  # 區域類型（健身房或游泳池）
    current_count = Column(Integer, nullable=False)  # 即時流量數量
    timestamp = Column(
        TIMESTAMP(timezone=True), default="CURRENT_TIMESTAMP"
    )  # 時間戳記
    __table_args__ = (
        CheckConstraint(
            "area_type IN ('gym', 'pool')", name="check_area_type"
        ),  # 檢查區域類型的有效性
    )


# 定義歷史統計的資料表模型
class HistoricalStats(Base):
    __tablename__ = "historical_stats"  # 資料表名稱

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )  # 唯一識別碼，使用 UUID
    center_id = Column(
        UUID(as_uuid=True), ForeignKey("sport_centers.id"), nullable=False
    )  # 關聯的運動中心 ID
    area_type = Column(String(20), nullable=False)  # 區域類型（健身房或游泳池）
    avg_count = Column(Float, nullable=False)  # 平均流量數量
    max_count = Column(Integer, nullable=False)  # 最大流量數量
    date = Column(Date, nullable=False)  # 統計日期
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())  # 建立時間
    updated_at = Column(
        TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now()
    )  # 更新時間
    __table_args__ = (
        CheckConstraint(
            "area_type IN ('gym', 'pool')", name="check_area_type_stats"
        ),  # 檢查區域類型的有效性
    )


# 定義用戶資料表模型
class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )  # 唯一識別碼，使用 UUID
    username = Column(String(100), nullable=False, unique=True)  # 用戶名稱，必填且唯一
    email = Column(String(255), nullable=True)  # 用戶電子郵件
    full_name = Column(String(255), nullable=True)  # 用戶全名
    role = Column(String(50), nullable=False)  # 用戶角色
    disabled = Column(Integer, nullable=False, default=0)  # 用戶是否被禁用
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())  # 建立時間
    updated_at = Column(
        TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now()
    )  # 更新時間
