"""
API 資料傳輸物件（DTO）定義
"""

from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum


class TimeRange(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class MaxCapacity(BaseModel):
    gym: int
    pool: int


class SportCenterResponse(BaseModel):
    id: str
    name: str
    zip: str
    address: str
    website_url: str
    max_capacity: MaxCapacity

    class Config:
        orm_mode = True


class CenterDetailResponse(SportCenterResponse):
    """單一運動中心詳細資訊"""

    pass


class FlowStatus(BaseModel):
    """區域即時人流狀態"""

    current_count: int
    max_capacity: int


class CenterFlowStatus(BaseModel):
    """運動中心即時人流狀態"""

    id: str
    name: str
    gym: FlowStatus
    pool: FlowStatus


class CurrentFlowsResponse(BaseModel):
    """所有運動中心即時人流回應"""

    timestamp: datetime
    centers: List[CenterFlowStatus]


class TrendDataPoint(BaseModel):
    """趨勢資料點"""

    timestamp: datetime
    count: int


class TrendStatsResponse(BaseModel):
    """趨勢統計資料回應"""

    center_id: str
    area_type: str
    data: List[TrendDataPoint]


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
