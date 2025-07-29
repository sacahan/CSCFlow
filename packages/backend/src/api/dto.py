from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict
from enum import Enum


class TimeRange(str, Enum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"


class SportCenterResponse(BaseModel):
    id: str
    name: str
    address: str
    zip_code: str
    website_url: str
    collector_type: str
    max_capacity: Dict[str, int]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class FlowDataResponse(BaseModel):
    current_count: int
    max_capacity: int
    timestamp: datetime


class HourlyStats(BaseModel):
    max: int
    min: int
    avg: float
    samples: int


class FlowStatsSummary(BaseModel):
    max: int
    min: int
    avg: float
    samples: int


class TimeRangeInfo(BaseModel):
    start: datetime
    end: datetime


class AreaStats(BaseModel):
    summary: FlowStatsSummary
    hourly_stats: Dict[int, HourlyStats]  # 小時為 key (0-23)
    time_range: TimeRangeInfo


class FlowStatsResponse(BaseModel):
    gym: Optional[AreaStats]
    pool: Optional[AreaStats]


class FlowCurrentResponse(BaseModel):
    gym: Optional[FlowDataResponse]
    pool: Optional[FlowDataResponse]
