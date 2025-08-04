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
from functools import wraps
import redis
import os
from dotenv import load_dotenv
import json
import jsonpickle  # 安裝：pip install jsonpickle
import logging

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Redis client using environment variables
redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    db=int(os.getenv("REDIS_DB")),
    password=os.getenv("REDIS_PASSWORD"),
)

# Retrieve Redis cache duration from environment variables
redis_cache_duration = int(os.getenv("REDIS_CACHE_DURATION", 3600))

# 建立主要路由器及子路由器
# router: 整合所有子路由的主要路由器
# centers_router: 處理運動中心相關的 API 端點
# auth_router: 處理認證相關的 API 端點
# flow_router: 處理人流資料相關的 API 端點
router = APIRouter()
centers_router = APIRouter(prefix="/api/v1/centers", tags=["centers"])
auth_router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
flow_router = APIRouter(prefix="/api/v1", tags=["flows"])
security = HTTPBearer()


def validate_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    session: AsyncSession = Depends(get_session),
):
    """
    驗證 JWT Token 的依賴函數

    此函數用於驗證使用者提供的 JWT Token 是否有效。

    Args:
        credentials (HTTPAuthorizationCredentials): 使用者提供的 JWT Token
        session (AsyncSession): 非同步資料庫會話

    Returns:
        HTTPAuthorizationCredentials: 驗證成功後的憑證物件

    Raises:
        HTTPException: 當 Token 無效或過期時拋出例外
    """
    auth_service = AuthService(session)
    auth_service.verify_token(credentials.credentials)
    return credentials


# Redis caching decorator
def cache_with_redis(key_prefix):
    """
    Decorator to cache function results in Redis.

    Args:
        key_prefix (str): Prefix for Redis keys.

    Returns:
        Function: Wrapped function with Redis caching.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 排除 kwargs 中的 session 與 credentials
            filtered_kwargs = {
                k: v for k, v in kwargs.items() if k not in ["session", "credentials"]
            }
            key = f"{key_prefix}:{json.dumps({'args': args, 'kwargs': filtered_kwargs}, default=str)}"

            # 嘗試從 Redis 取得快取結果
            cached_result = redis_client.get(key)
            if cached_result:
                # 使用 jsonpickle 反序列化
                logger.info(f"🔄 由 Redis 快取取得: {key}")
                return jsonpickle.loads(cached_result)

            # 執行原始函數並取得結果
            result = await func(*args, **kwargs)

            # 使用 jsonpickle 序列化並存入 Redis
            redis_client.setex(key, redis_cache_duration, jsonpickle.dumps(result))
            return result

        return wrapper

    return decorator


# 運動中心管理 API
@centers_router.get("/", response_model=List[SportCenterResponse])
@cache_with_redis("sport_centers")
async def get_sport_centers(
    session: AsyncSession = Depends(get_session),  # 注入資料庫會話
    credentials: HTTPAuthorizationCredentials = Depends(validate_token),
):
    """
    取得所有運動中心的基本資訊

    此端點返回所有運動中心的基本資訊列表。

    Args:
        session (AsyncSession): 非同步資料庫會話
        credentials (HTTPAuthorizationCredentials): 驗證後的使用者憑證

    Returns:
        List[SportCenterResponse]: 運動中心基本資訊列表
    """
    flow_service = FlowService(session)
    centers = flow_service.get_all_centers()
    return centers


@centers_router.get("/{zip_code}", response_model=CenterDetailResponse)
@cache_with_redis("center_detail")
async def get_center_detail(
    zip_code: str,  # 運動中心郵遞區號
    session: AsyncSession = Depends(get_session),
    credentials: HTTPAuthorizationCredentials = Depends(validate_token),
):
    """
    取得指定郵遞區號的運動中心詳細資訊

    此端點根據郵遞區號返回運動中心的詳細資訊。

    Args:
        zip_code (str): 運動中心郵遞區號
        session (AsyncSession): 非同步資料庫會話
        credentials (HTTPAuthorizationCredentials): 驗證後的使用者憑證

    Returns:
        CenterDetailResponse: 運動中心詳細資訊

    Raises:
        HTTPException: 當找不到運動中心資料時拋出例外
    """
    flow_service = FlowService(session)
    center = flow_service.get_center_detail_by_zip(zip_code)
    if not center:
        raise HTTPException(status_code=404, detail="找不到運動中心資料")
    return center


# 即時人流數據 API
@flow_router.get("/current_flows", response_model=CurrentFlowsResponse)
async def get_current_flows(
    zip_code: str = Query(..., description="運動中心郵遞區號"),
    session: AsyncSession = Depends(get_session),
    credentials: HTTPAuthorizationCredentials = Depends(validate_token),
):
    """
    取得指定運動中心的即時人流數據

    此端點返回指定運動中心的即時人流數據。

    Args:
        zip_code (str): 運動中心郵遞區號
        session (AsyncSession): 非同步資料庫會話
        credentials (HTTPAuthorizationCredentials): 驗證後的使用者憑證

    Returns:
        CurrentFlowsResponse: 即時人流數據
    """
    flow_service = FlowService(session)
    flows = await flow_service.get_current_flows(zip_code)
    return flows


@flow_router.get("/trend_stats", response_model=TrendStatsResponse)
@cache_with_redis("trend_stats")
async def get_trend_stats(
    zip_code: str = Query(..., description="運動中心郵遞區號"),
    area_type: str = Query(None, description="區域類型：gym 或 pool"),
    time_range: str = Query(..., description="時間範圍：daily、weekly、monthly"),
    session: AsyncSession = Depends(get_session),
    credentials: HTTPAuthorizationCredentials = Depends(validate_token),
):
    """
    取得指定運動中心的趨勢統計數據

    此端點返回指定運動中心的趨勢統計數據，根據區域類型與時間範圍進行篩選。

    Args:
      zip_code (str): 運動中心郵遞區號
      area_type (str): 區域類型（gym 或 pool）
      time_range (str): 時間範圍（daily、weekly、monthly）
      session (AsyncSession): 非同步資料庫會話
      credentials (HTTPAuthorizationCredentials): 驗證後的使用者憑證

    Returns:
      TrendStatsResponse: 趨勢統計數據

    Raises:
      HTTPException: 當 area_type 無效或找不到統計資料時拋出例外
    """
    if area_type and area_type not in ["gym", "pool"]:
        raise HTTPException(
            status_code=400,
            detail={
                "status": 400,
                "code": "InvalidParameter",
                "message": "area_type 必須為 'gym', 'pool' 或為空值",
                "details": {"field": "area_type"},
            },
        )

    if time_range not in ["daily", "weekly", "monthly"]:
        raise HTTPException(
            status_code=400,
            detail={
                "status": 400,
                "code": "InvalidParameter",
                "message": "time_range 必須為 'daily'、'weekly' 或 'monthly'",
                "details": {"field": "time_range"},
            },
        )

    # 初始化 FlowService 並取得趨勢統計數據
    flow_service = FlowService(session)
    stats = await flow_service.get_trend_stats(zip_code, area_type, time_range)
    if not stats:
        raise HTTPException(status_code=404, detail="找不到統計資料")

    return stats


# 認證 API
@auth_router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, session: AsyncSession = Depends(get_session)):
    """
    使用者登入
    """
    auth_service = AuthService(session)
    try:
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
        return LoginResponse(**result)  # 確保結果符合 LoginResponse 模型
    except Exception as e:
        logger.error(f"登入時發生錯誤: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "status": 500,
                "code": "InternalServerError",
                "message": "登入處理時發生錯誤",
                "details": None,
            },
        )


# 健康檢查 API
@router.get("/health", response_model=HealthCheckResponse, tags=["health"])
async def health_check(session: AsyncSession = Depends(get_session)):
    """
    系統健康狀態檢查

    此端點檢查系統的健康狀態，包括資料庫與快取狀態。

    Args:
        session (AsyncSession): 非同步資料庫會話

    Returns:
        HealthCheckResponse: 系統健康狀態，包括資料庫與快取狀態
    """
    try:
        # 檢查資料庫連線
        await session.execute("SELECT 1")
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    # Redis connection check
    try:
        redis_client.ping()
        cache_status = "connected"
    except redis.ConnectionError:
        cache_status = "disconnected"

    return {"status": "ok", "database": db_status, "cache": cache_status}


# 註冊路由
router.include_router(centers_router)
router.include_router(auth_router)
router.include_router(flow_router)

# 導出 API 路由
api_router = router
