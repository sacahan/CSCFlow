"""
運動中心資料庫存取
"""

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .base_repository import BaseRepository
from ..models.sport_center import SportCenter


class SportCenterRepository(BaseRepository[SportCenter]):
    """運動中心資料庫存取類別"""

    def __init__(self, session: AsyncSession):
        super().__init__(session, SportCenter)

    async def get_active_centers(self) -> List[SportCenter]:
        """取得所有啟用中的運動中心"""
        result = await self.session.execute(
            select(SportCenter).filter(SportCenter.is_active)
        )
        return result.scalars().all()

    async def get_by_type(self, collector_type: str) -> List[SportCenter]:
        """依收集器類型取得運動中心"""
        result = await self.session.execute(
            select(SportCenter).filter(SportCenter.collector_type == collector_type)
        )
        return result.scalars().all()

    async def get_by_area(self, area_code: str) -> List[SportCenter]:
        """依地區取得運動中心"""
        result = await self.session.execute(
            select(SportCenter).filter(SportCenter.zip_code.startswith(area_code))
        )
        return result.scalars().all()
