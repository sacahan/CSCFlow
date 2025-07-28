from pydantic import BaseModel
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime


# 用戶角色定義
class UserRole(str, Enum):
    ADMIN = "admin"  # 系統管理員角色，具有最高權限
    STAFF = "staff"  # 運動中心職員角色，負責日常管理
    IOT_DEVICE = "iot_device"  # IoT設備角色，用於設備間的交互


# 用戶相關模型
class User(BaseModel):
    username: str  # 用戶名，唯一標識用戶
    email: Optional[str] = None  # 用戶的電子郵件地址，可選
    full_name: Optional[str] = None  # 用戶的全名，可選
    role: UserRole  # 用戶角色，定義用戶的權限範圍
    disabled: bool = False  # 用戶是否被禁用，預設為未禁用


class UserAuth(BaseModel):
    username: str  # 用戶名，用於身份驗證
    password: str  # 密碼，用於身份驗證


class TokenResponse(BaseModel):
    access_token: str  # 用於身份驗證的訪問令牌
    token_type: str  # 訪問令牌的類型，例如 "Bearer"
    expires_in: int  # 訪問令牌的有效期（秒）
    user: User  # 與令牌相關聯的用戶資訊


# 運動中心相關模型
class OperationHours(BaseModel):
    open: str  # 運動中心的開放時間
    close: str  # 運動中心的關閉時間


class LocationInfo(BaseModel):
    lat: float  # 地理位置的緯度
    lng: float  # 地理位置的經度
    place_id: str  # Google Maps的地點唯一識別碼


class MaxCapacity(BaseModel):
    gym: int  # 健身房的最大容量
    pool: int  # 游泳池的最大容量


class SportCenterResponse(BaseModel):
    id: str  # 運動中心的唯一識別碼（UUID）
    name: str  # 運動中心的名稱
    address: str  # 運動中心的地址
    formatted_address: str  # 格式化後的地址
    location: LocationInfo  # 運動中心的地理位置資訊
    max_capacity: MaxCapacity  # 運動中心的最大容量資訊

    class Config:
        orm_mode = True  # 啟用ORM模式，允許從ORM對象轉換


# 流量相關模型
class AreaStats(BaseModel):
    current_count: int  # 區域內的當前人數
    max_capacity: int  # 區域的最大容量
    percentage: float  # 區域內人數占最大容量的百分比


class RealTimeFlowResponse(BaseModel):
    id: str  # 運動中心的唯一識別碼
    name: str  # 運動中心的名稱
    gym: AreaStats  # 健身房的流量資訊
    pool: AreaStats  # 游泳池的流量資訊


class UpdateFlowRequest(BaseModel):
    center_id: str  # 運動中心的唯一識別碼
    area_type: str  # 區域類型（健身房或游泳池）
    count: int  # 更新的流量數量


# 統計相關模型
class FlowDataPoint(BaseModel):
    timestamp: datetime  # 流量數據的時間戳
    count: int  # 流量數據中的人數
    percentage: float  # 流量數據中的百分比


class TrendStatsResponse(BaseModel):
    center_id: str  # 運動中心的唯一識別碼
    area_type: str  # 區域類型（健身房或游泳池）
    data: List[FlowDataPoint]  # 包含統計資料的列表


# 附近運動中心相關模型
class NearbyCenterStats(BaseModel):
    current_count: int  # 附近運動中心的當前人數
    percentage: float  # 附近運動中心的流量百分比


class NearbyCenterResponse(BaseModel):
    id: str  # 附近運動中心的唯一識別碼
    name: str  # 附近運動中心的名稱
    formatted_address: str  # 附近運動中心的格式化地址
    location: LocationInfo  # 附近運動中心的地理位置資訊
    distance: float  # 與當前位置的距離（公里）
    current_stats: Dict[str, NearbyCenterStats]  # 附近運動中心的流量統計資訊


class NearbyCentersResponse(BaseModel):
    centers: List[NearbyCenterResponse]  # 附近運動中心的列表
