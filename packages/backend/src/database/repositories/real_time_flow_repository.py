"""
即時人流資料庫存取
"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from .base_repository import BaseRepository
from ..models.real_time_flow import RealTimeFlow


class RealTimeFlowRepository(BaseRepository[RealTimeFlow]):
    """即時人流資料庫存取類別"""

    def __init__(self, session: AsyncSession):
        super().__init__(session, RealTimeFlow)

    async def get_latest_flow(
        self, center_id: str, area_type: str
    ) -> Optional[RealTimeFlow]:
        """取得最新的流量資料"""
        result = await self.session.execute(
            select(RealTimeFlow)
            .filter(
                and_(
                    RealTimeFlow.center_id == center_id,
                    RealTimeFlow.area_type == area_type,
                )
            )
            .order_by(RealTimeFlow.timestamp.desc())
            .limit(1)
        )
        return result.scalars().first()

    async def get_flows_by_time_range(
        self, center_id: str, area_type: str, start_time: datetime, end_time: datetime
    ) -> List[RealTimeFlow]:
        """取得指定時間範圍的流量資料"""
        result = await self.session.execute(
            select(RealTimeFlow)
            .filter(
                and_(
                    RealTimeFlow.center_id == center_id,
                    RealTimeFlow.area_type == area_type,
                    RealTimeFlow.timestamp >= start_time,
                    RealTimeFlow.timestamp <= end_time,
                )
            )
            .order_by(RealTimeFlow.timestamp)
        )
        return result.scalars().all()

    async def get_today_flows(
        self, center_id: str, area_type: str
    ) -> List[RealTimeFlow]:
        """取得今天的流量資料"""
        today = datetime.now().date()
        start_time = datetime.combine(today, datetime.min.time())
        end_time = datetime.combine(today, datetime.max.time())
        return await self.get_flows_by_time_range(
            center_id, area_type, start_time, end_time
        )
