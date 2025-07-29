from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import logging
from typing import List
from packages.backend.src.database.models import SportCenter, RealTimeFlow
from ..collectors.factory import CollectorFactory
from ..database.db import AsyncSession, get_session

logger = logging.getLogger(__name__)


class FlowScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    async def start(self):
        """啟動排程器"""
        self.scheduler.add_job(
            self._collect_all_centers_flow,
            CronTrigger(minute="*/5"),  # 每5分鐘執行
            id="collect_flow_data",
            replace_existing=True,
        )
        self.scheduler.start()
        logger.info("流量收集排程已啟動")

    async def shutdown(self):
        """關閉排程器"""
        self.scheduler.shutdown()
        logger.info("流量收集排程已關閉")

    async def _collect_all_centers_flow(self):
        """收集所有運動中心的即時資料"""
        async with get_session() as session:
            centers = await self._get_active_centers(session)
            logger.info(f"開始收集 {len(centers)} 個運動中心的資料")

            for center in centers:
                try:
                    collector = CollectorFactory.create_collector(
                        center.collector_type, center.collector_config
                    )

                    flow_data = await collector.collect_flow_data()

                    if collector.validate_response(flow_data):
                        await self._save_flow_data(
                            session, center.id, flow_data, center.max_capacity
                        )
                        logger.info(f"成功收集資料 - {center.name}")
                    else:
                        logger.error(f"資料驗證失敗 - {center.name}")

                except Exception as e:
                    logger.error(f"收集資料失敗 - {center.name}: {str(e)}")
                    continue

    async def _get_active_centers(self, session: AsyncSession) -> List[SportCenter]:
        """取得所有啟用中的運動中心"""
        return await session.query(SportCenter).filter_by(is_active=True).all()

    async def _save_flow_data(
        self,
        session: AsyncSession,
        center_id: str,
        flow_data: dict,
        max_capacity: dict,
    ):
        """儲存收集到的流量資料"""
        now = datetime.now()

        for area_type in ["gym", "pool"]:
            if area_type in flow_data and area_type in max_capacity:
                flow = RealTimeFlow(
                    center_id=center_id,
                    area_type=area_type,
                    current_count=flow_data[area_type],
                    max_capacity=max_capacity[area_type],
                    timestamp=now,
                )
                session.add(flow)

        await session.commit()
