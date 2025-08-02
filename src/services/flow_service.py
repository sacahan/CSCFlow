"""
流量服務
處理運動中心人流相關的業務邏輯
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from ..database.repositories import RealTimeFlowRepository, HistoricalStatsRepository
from ..collectors.center_loader import CenterLoader
from ..api.dto import TrendStats, TrendStatsResponse

logger = logging.getLogger(__name__)


# FlowService 類別負責處理運動中心人流相關的業務邏輯
class FlowService:
    def __init__(self, session: AsyncSession):
        # 初始化 FlowService
        self.session = session
        self.flow_repository = RealTimeFlowRepository(session)
        self.stats_repository = HistoricalStatsRepository(session)
        self.center_loader = CenterLoader()

    def get_all_centers(self) -> List[Dict[str, Any]]:
        """取得所有運動中心列表"""

        centers_config = self.center_loader.get_all_centers()
        return sorted(
            [
                {
                    "name": center_info["basic_info"]["name"],
                    "zip_code": center_info["basic_info"]["zip_code"],
                    "address": center_info["basic_info"]["address"],
                    "website_url": center_info["basic_info"]["website_url"],
                    "facility_info": center_info["facility_info"],
                }
                for center_info in centers_config.values()
            ],
            key=lambda center: center["zip_code"],
        )

    def get_center_detail_by_zip(self, zip_code: str) -> Optional[Dict[str, Any]]:
        """取得特定運動中心詳情"""
        center = self.center_loader.get_center_by_zip(zip_code)
        if not center:
            return None

        center_id, center_info = next(iter(center.items()))
        return {
            "name": center_info["basic_info"]["name"],
            "zip_code": center_info["basic_info"]["zip_code"],
            "address": center_info["basic_info"]["address"],
            "website_url": center_info["basic_info"]["website_url"],
            "facility_info": center_info["facility_info"],
        }

    async def get_current_flows(self, zip_code: str) -> Dict[str, Any]:
        """取得即時人流數據"""
        # 取得運動中心資訊
        center = self.center_loader.get_center_by_zip(zip_code)
        if not center:
            return {"timestamp": datetime.now(), "center": {}}

        center_id, center_info = next(iter(center.items()))

        # 初始化運動中心的流量資料
        center_flow = {
            "zip_code": center_info["basic_info"]["zip_code"],
            "name": center_info["basic_info"]["name"],
            "gym": {
                "available": center_info["facility_info"]["gym"]["available"],
                "current_count": 0,
                "max_capacity": center_info["facility_info"]["gym"]["max_capacity"],
                "last_updated": datetime.now(),
            },
            "pool": {
                "available": center_info["facility_info"]["pool"]["available"],
                "current_count": 0,
                "max_capacity": center_info["facility_info"]["pool"]["max_capacity"],
                "last_updated": datetime.now(),
            },
        }

        # 取得最新流量資料，更新流量數據
        for area_type in ["gym", "pool"]:
            if center_info["facility_info"][area_type]["available"]:
                flow = await self.flow_repository.get_latest_flow(zip_code, area_type)
                if flow:
                    center_flow[area_type]["current_count"] = flow.current_count
                    center_flow[area_type]["last_updated"] = (
                        flow.timestamp.astimezone().strftime("%Y-%m-%d %H:%M:%S")
                    )

        # 返回包含時間戳和運動中心流量資料的結果
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "center": center_flow,
        }

    async def get_trend_stats(
        self, zip_code: str, area_type: str, time_range: str
    ) -> TrendStatsResponse:
        """取得趨勢統計資料"""

        if time_range not in ["daily", "weekly", "monthly"]:
            raise ValueError("無效的時間範圍")

        if time_range == "daily":
            start_date = datetime.now().replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            end_date = datetime.now()
        elif time_range == "weekly":
            start_date = datetime.now() - timedelta(days=7)
            end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        elif time_range == "monthly":
            start_date = datetime.now() - timedelta(days=30)
            end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # 從資料庫取得最新的統計資料
        if area_type == "gym":
            gym_stats = await self.stats_repository.get_stats_by_time_range(
                zip_code, "gym", time_range, start_date, end_date
            )
            pool_stats = []
        elif area_type == "pool":
            gym_stats = []
            pool_stats = await self.stats_repository.get_stats_by_time_range(
                zip_code, "pool", time_range, start_date, end_date
            )
        else:
            gym_stats = await self.stats_repository.get_stats_by_time_range(
                zip_code, "gym", time_range, start_date, end_date
            )
            pool_stats = await self.stats_repository.get_stats_by_time_range(
                zip_code, "pool", time_range, start_date, end_date
            )

        # 處理 gym_stats 列表
        gym_stats_result = [
            TrendStats(
                date_time=stat.start_date,
                avg_count=stat.avg_count,
                max_count=stat.max_count,
                min_count=stat.min_count,
            )
            for stat in gym_stats
        ]

        # 處理 pool_stats 列表
        pool_stats_result = [
            TrendStats(
                date_time=stat.start_date,
                avg_count=stat.avg_count,
                max_count=stat.max_count,
                min_count=stat.min_count,
            )
            for stat in pool_stats
        ]

        return TrendStatsResponse(
            zip_code=zip_code,
            stats_type=time_range,
            gym=gym_stats_result,
            pool=pool_stats_result,
        )
