from typing import Dict, Any
from datetime import datetime
import logging
from packages.backend.src.database.repositories.sport_center_repository import (
    SportCenterRepository,
)
from packages.backend.src.database.repositories.real_time_flow_repository import (
    RealTimeFlowRepository,
)
from packages.backend.src.collectors.factory import CollectorFactory
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class FlowService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.sport_center_repository = SportCenterRepository(session)
        self.flow_repository = RealTimeFlowRepository(session)

    async def collect_all_centers_flow(self):
        """收集所有運動中心的即時資料"""
        centers = await self.sport_center_dao.get_active_centers()
        logger.info(f"開始收集 {len(centers)} 個運動中心的資料")

        for center in centers:
            try:
                collector = CollectorFactory.create_collector(
                    center.collector_type, center.collector_config
                )

                flow_data = await collector.collect_flow_data()

                if collector.validate_response(flow_data):
                    for area_type, count in flow_data.items():
                        await self.flow_dao.create(
                            center_id=center.id,
                            area_type=area_type,
                            current_count=count,
                            max_capacity=center.max_capacity[area_type],
                            timestamp=datetime.now(),
                        )
                    logger.info(f"成功收集資料 - {center.name}")
                else:
                    logger.error(f"資料驗證失敗 - {center.name}")

            except Exception as e:
                logger.error(f"收集資料失敗 - {center.name}: {str(e)}")

    async def get_center_current_flow(self, center_id: str) -> Dict[str, Any]:
        """取得運動中心當前流量"""
        result = {}
        for area_type in ["gym", "pool"]:
            flow = await self.flow_dao.get_latest_flow(center_id, area_type)
            if flow:
                result[area_type] = {
                    "current_count": flow.current_count,
                    "max_capacity": flow.max_capacity,
                    "timestamp": flow.timestamp,
                }
        return result

    async def get_center_today_stats(self, center_id: str) -> Dict[str, Any]:
        """取得運動中心今日統計資料"""
        result = {}
        for area_type in ["gym", "pool"]:
            flows = await self.flow_dao.get_today_flows(center_id, area_type)
            if flows:
                counts = [flow.current_count for flow in flows]
                result[area_type] = {
                    "max": max(counts),
                    "min": min(counts),
                    "avg": sum(counts) / len(counts),
                    "samples": len(counts),
                }
        return result
