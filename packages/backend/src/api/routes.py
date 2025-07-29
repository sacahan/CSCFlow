from fastapi import APIRouter, Depends, HTTPException, Query, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .dto import (
    SportCenterResponse,
    TrendStatsResponse,
    LoginRequest,
    LoginResponse,
    CenterDetailResponse,
    HealthCheckResponse,
    CurrentFlowsResponse,
)
from ..services.flow_service import FlowService
from ..services.auth_service import AuthService
from ..database.db import get_session

# 建立路由器實例
# router: 主要路由器，用於整合所有子路由
# centers_router: 處理運動中心相關的 API 端點
# auth_router: 處理認證相關的 API 端點
# flow_router: 處理人流資料相關的 API 端點
router = APIRouter()
centers_router = APIRouter(prefix="/api/v1/centers", tags=["centers"])
auth_router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
flow_router = APIRouter(prefix="/api/v1", tags=["flows"])
security = HTTPBearer()


# 運動中心管理 API
@centers_router.get("/", response_model=List[SportCenterResponse])
async def get_sport_centers(
    session: AsyncSession = Depends(get_session),  # 注入資料庫會話
    credentials: HTTPAuthorizationCredentials = Security(security),  # JWT 認證
):
    """
    取得所有運動中心列表
    - 需要認證權限
    - 返回所有運動中心的基本資訊列表
    """
    flow_service = FlowService(session)
    centers = await flow_service.get_all_centers()
    return centers


@centers_router.get("/{zip_code}", response_model=CenterDetailResponse)
async def get_center_detail(
    zip_code: str,  # 運動中心郵遞區號
    session: AsyncSession = Depends(get_session),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    """
    取得特定運動中心詳情
    - 需要認證權限
    - zip_code: 運動中心郵遞區號
    - 返回指定運動中心的詳細資訊
    - 如果找不到指定的運動中心，回傳 404 錯誤
    """
    flow_service = FlowService(session)
    center = await flow_service.get_center_detail_by_zip(zip_code)
    if not center:
        raise HTTPException(status_code=404, detail="找不到運動中心資料")
    return center


# 即時人流數據 API
@flow_router.get("/current_flows", response_model=CurrentFlowsResponse)
async def get_current_flows(
    zip_code: str = Query(..., description="運動中心郵遞區號"),
    session: AsyncSession = Depends(get_session),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    """
    取得指定運動中心的即時人流數據
    - zip_code: 運動中心郵遞區號（必填）
    - 返回指定運動中心的即時人流資料
    """
    flow_service = FlowService(session)
    flows = await flow_service.get_current_flows(zip_code)
    return flows


@flow_router.get("/trend_stats", response_model=TrendStatsResponse)
async def get_trend_stats(
    zip_code: str = Query(..., description="運動中心郵遞區號"),
    area_type: str = Query(..., description="區域類型：gym 或 pool"),
    time_range: str = Query(..., description="時間範圍：daily、weekly、monthly"),
    session: AsyncSession = Depends(get_session),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    """取得趨勢統計數據"""
    if area_type not in ["gym", "pool"]:
        raise HTTPException(
            status_code=400,
            detail={
                "status": 400,
                "code": "InvalidParameter",
                "message": "area_type 必須為 'gym' 或 'pool'",
                "details": {"field": "area_type"},
            },
        )

    flow_service = FlowService(session)
    stats = await flow_service.get_trend_stats(zip_code, area_type, time_range)
    if not stats:
        raise HTTPException(status_code=404, detail="找不到統計資料")
    return stats


# 認證 API
@auth_router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, session: AsyncSession = Depends(get_session)):
    """使用者登入"""
    auth_service = AuthService(session)
    result = await auth_service.authenticate(request.username, request.password)
    if not result:
        raise HTTPException(
            status_code=401,
            detail={
                "status": 401,
                "code": "InvalidCredentials",
                "message": "帳號或密碼錯誤",
                "details": None,
            },
        )
    return result


# 健康檢查 API
@router.get("/health", response_model=HealthCheckResponse, tags=["health"])
async def health_check(session: AsyncSession = Depends(get_session)):
    """系統健康狀態檢查"""
    try:
        # 檢查資料庫連線
        await session.execute("SELECT 1")
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    # TODO: 實作 Redis 連線檢查
    cache_status = "ok"

    return {"status": "ok", "database": db_status, "cache": cache_status}


# 註冊路由
router.include_router(centers_router)
router.include_router(auth_router)
router.include_router(flow_router)

# 導出 API 路由
api_router = router
