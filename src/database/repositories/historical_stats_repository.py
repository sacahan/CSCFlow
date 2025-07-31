"""
歷史統計資料庫存取
"""

from typing import List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, func
from ..models.historical_stats import HistoricalStats


class HistoricalStatsRepository:
    """歷史統計資料庫存取類別"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = HistoricalStats

    async def get_stats_by_time_range(
        self,
        zip_code: str,
        area_type: str,
        time_range: str,
        start_date: datetime,
        end_date: datetime,
    ) -> List[HistoricalStats]:
        """取得指定時間範圍的統計資料

        Args:
            zip_code (str): 運動中心郵遞區號
            area_type (str): 區域類型 (gym 或 pool)
            time_range (str): 統計類型 (daily, weekly, monthly)
            start_date (datetime): 開始時間
            end_date (datetime): 結束時間

        Returns:
            List[HistoricalStats]: 符合條件的統計資料列表
        """

        # time_range = daily 時，self.model.stats_type = 'hourly' , group by self.model.start_date 到 小時
        # time_range = weekly 時，self.model.stats_type = 'daily' , group by group by self.model.start_date 到天
        # time_range = monthly 時，self.model.stats_type = 'daily' , group by group by self.model.start_date 到天
        if time_range == "daily":
            stats_type = "hourly"
        elif time_range == "weekly":
            stats_type = "daily"
        elif time_range == "monthly":
            stats_type = "daily"
        else:
            raise ValueError("Invalid time range specified")

        result = await self.session.execute(
            select(
                self.model.zip_code,
                self.model.area_type,
                self.model.stats_type,
                self.model.start_date,
                func.avg(self.model.avg_count).label("avg_count"),
                func.max(self.model.max_count).label("max_count"),
                func.min(self.model.min_count).label("min_count"),
            )
            .filter(
                and_(
                    self.model.zip_code == zip_code,
                    self.model.area_type == area_type,
                    self.model.stats_type == stats_type,
                    self.model.start_date >= start_date,
                    self.model.end_date <= end_date,
                )
            )
            .group_by(
                self.model.zip_code,
                self.model.area_type,
                self.model.stats_type,
                self.model.start_date,
            )
            .order_by(self.model.start_date.asc())
        )

        # 使用 SQLAlchemy 的 mapping 功能
        mapped_result = result.scalars().all()
        return mapped_result
