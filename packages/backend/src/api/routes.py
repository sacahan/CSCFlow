from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .dto import SportCenterResponse, FlowStatsResponse, FlowCurrentResponse, TimeRange
from ..services.flow_service import FlowService
from ..db import get_session

router = APIRouter(prefix="/api/sport-centers", tags=["sport-centers"])


@router.get("/", response_model=List[SportCenterResponse])
async def get_sport_centers(session: AsyncSession = Depends(get_session)):
    """取得所有運動中心列表"""
    flow_service = FlowService(session)
    centers = await flow_service.get_all_centers()
    return centers


@router.get("/{center_id}/flow", response_model=FlowCurrentResponse)
async def get_center_flow(center_id: str, session: AsyncSession = Depends(get_session)):
    """
    取得運動中心即時流量
    - 返回健身房和游泳池的即時人數
    - 包含最大容留人數和最後更新時間
    """
    flow_service = FlowService(session)
    flow = await flow_service.get_center_current_flow(center_id)
    if not flow:
        raise HTTPException(status_code=404, detail="找不到運動中心資料")
    return flow


@router.get("/{center_id}/stats", response_model=FlowStatsResponse)
async def get_center_stats(
    center_id: str,
    time_range: TimeRange = Query(
        TimeRange.DAY, description="統計時間範圍：day(今日)、week(本週)、month(本月)"
    ),
    session: AsyncSession = Depends(get_session),
):
    """
    取得運動中心統計資料
    - 支援日、週、月的統計資料
    - 提供每小時的統計摘要
    - 包含最大、最小、平均人數和樣本數
    """
    flow_service = FlowService(session)
    stats = await flow_service.get_center_stats(center_id, time_range)
    if not stats:
        raise HTTPException(status_code=404, detail="找不到運動中心資料")
    return stats
