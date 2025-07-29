"""
即時人流資料庫存取
"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, update, delete
from ..models.real_time_flow import RealTimeFlow


class RealTimeFlowRepository:
    """即時人流資料庫存取類別"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = RealTimeFlow

    async def get(self, id: int) -> Optional[RealTimeFlow]:
        """依 ID 取得單一記錄"""
        result = await self.session.execute(
            select(self.model).filter(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> List[RealTimeFlow]:
        """取得所有記錄"""
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def add(self, entity: RealTimeFlow) -> RealTimeFlow:
        """新增記錄"""
        self.session.add(entity)
        await self.session.commit()
        return entity

    async def update(self, id: int, values: dict) -> Optional[RealTimeFlow]:
        """更新記錄"""
        await self.session.execute(
            update(self.model).where(self.model.id == id).values(**values)
        )
        await self.session.commit()
        return await self.get(id)

    async def delete(self, id: int) -> bool:
        """刪除記錄"""
        result = await self.session.execute(
            delete(self.model).where(self.model.id == id)
        )
        await self.session.commit()
        return result.rowcount > 0

    async def get_latest_flow(
        self, zip_code: str, area_type: str
    ) -> Optional[RealTimeFlow]:
        """取得最新的流量資料"""
        result = await self.session.execute(
            select(self.model)
            .filter(
                and_(
                    self.model.zip_code == zip_code,
                    self.model.area_type == area_type,
                )
            )
            .order_by(self.model.timestamp.desc())
            .limit(1)
        )
        return result.scalars().first()

    async def get_flows_by_time_range(
        self, zip_code: str, area_type: str, start_time: datetime, end_time: datetime
    ) -> List[RealTimeFlow]:
        """取得指定時間範圍的流量資料"""
        result = await self.session.execute(
            select(self.model)
            .filter(
                and_(
                    self.model.zip_code == zip_code,
                    self.model.area_type == area_type,
                    self.model.timestamp >= start_time,
                    self.model.timestamp <= end_time,
                )
            )
            .order_by(self.model.timestamp)
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
