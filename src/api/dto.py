"""
API 資料傳輸物件（DTO）定義
"""

from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum


class TimeRange(str, Enum):
    """時間範圍選項"""

    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class Capacity(BaseModel):
    """運動中心設施容量資訊"""

    available: bool
    max_capacity: Optional[int]


class FacilityInfo(BaseModel):
    """運動中心設施資訊"""

    gym: Capacity
    pool: Capacity


class SportCenterResponse(BaseModel):
    """運動中心基本資訊"""

    name: str
    zip_code: str
    address: str
    website_url: str
    facility_info: FacilityInfo
    status: bool = True


class CenterDetailResponse(SportCenterResponse):
    """單一運動中心詳細資訊"""

    pass


class FlowStatus(BaseModel):
    """區域即時人流狀態"""

    current_count: Optional[int] = 0
    max_capacity: Optional[int] = None
    last_updated: datetime


class CenterFlowStatus(BaseModel):
    """運動中心即時人流狀態"""

    zip_code: str
    name: str
    gym: FlowStatus
    pool: FlowStatus


class CurrentFlowsResponse(BaseModel):
    """所有運動中心即時人流回應"""

    timestamp: datetime
    centers: List[CenterFlowStatus]


class TrendStats(BaseModel):
    """趨勢統計數據"""

    date_time: datetime
    avg_count: int
    max_count: int
    min_count: int


class TrendStatsResponse(BaseModel):
    """趨勢統計資料回應"""

    zip_code: str
    area_type: str
    time_range: str
    stats: TrendStats


class LoginRequest(BaseModel):
    """登入請求"""

    username: str
    password: str


class LoginResponse(BaseModel):
    """登入回應"""

    access_token: str
    expires_in: int


class HealthCheckResponse(BaseModel):
    """健康檢查回應"""

    status: str
    database: str
    cache: str


class ErrorResponse(BaseModel):
    """錯誤回應"""

    status: int
    code: str
    message: str
    details: Optional[Dict] = None


class CollectorConfig(BaseModel):
    """API Collector 配置"""

    endpoints: List[str]
    method: str
    headers: Optional[Dict[str, str]]
    response_mapping: Dict[str, Dict[str, Optional[int]]]


class SportCenterCollector(BaseModel):
    """運動中心收集器"""

    type: str
    config: CollectorConfig
