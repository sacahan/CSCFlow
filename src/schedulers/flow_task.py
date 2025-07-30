from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import logging
from typing import List
from ..database.models import SportCenter, RealTimeFlow
from ..collectors.factory import CollectorFactory
from ..database.db import AsyncSession, AsyncSessionLocal

logger = logging.getLogger(__name__)


class FlowTask:
    def __init__(self):
        """初始化 FlowTask 類別，建立非同步排程器"""
        self.scheduler = AsyncIOScheduler()

    async def start(self):
        """
        啟動排程器並新增收集流量資料的排程任務。
        排程任務每 5 分鐘執行一次。
        """
        self.scheduler.add_job(
            self._collect_all_centers_flow,
            CronTrigger(minute="*/5"),  # 每5分鐘執行
            id="collect_flow_data",
            replace_existing=True,
        )
        self.scheduler.start()
        logger.info("流量收集排程已啟動")

    async def shutdown(self):
        """
        關閉排程器，停止所有排程任務。
        """
        self.scheduler.shutdown()
        logger.info("流量收集排程已關閉")

    async def _collect_all_centers_flow(self):
        """
        收集所有啟用中的運動中心的即時流量資料。
        使用 CollectorFactory 根據運動中心的設定建立資料收集器。
        """
        async with AsyncSessionLocal() as session:
            centers = await self._get_active_centers(session)
            logger.info(f"開始收集 {len(centers)} 個運動中心的資料")

            for center in centers:
                try:
                    # 根據運動中心的收集器類型與設定建立資料收集器
                    collector = CollectorFactory.create_collector(
                        center.collector_type, center.collector_config
                    )

                    # 收集即時流量資料
                    flow_data = await collector.collect_flow_data()

                    # 驗證收集到的資料是否正確
                    if collector.validate_response(flow_data):
                        await self._save_flow_data(
                            session, center.id, flow_data, center.max_capacity
                        )
                        logger.info(f"成功收集資料 - {center.name}")
                    else:
                        logger.error(f"資料驗證失敗 - {center.name}")

                except Exception as e:
                    # 捕捉例外並記錄錯誤訊息
                    logger.error(f"收集資料失敗 - {center.name}: {str(e)}")
                    continue

    async def _get_active_centers(self, session: AsyncSession) -> List[SportCenter]:
        """
        從資料庫中取得所有啟用中的運動中心。

        :param session: 非同步資料庫會話
        :return: 啟用中的運動中心列表
        """
        return await session.query(SportCenter).filter_by(is_active=True).all()

    async def _save_flow_data(
        self,
        session: AsyncSession,
        center_id: str,
        flow_data: dict,
        max_capacity: dict,
    ):
        """
        將收集到的流量資料儲存到資料庫中。

        :param session: 非同步資料庫會話
        :param center_id: 運動中心的唯一識別碼
        :param flow_data: 收集到的流量資料
        :param max_capacity: 運動中心的最大容量設定
        """
        now = datetime.now()

        for area_type in ["gym", "pool"]:
            if area_type in flow_data and area_type in max_capacity:
                # 建立 RealTimeFlow 實例並新增到資料庫
                flow = RealTimeFlow(
                    center_id=center_id,
                    area_type=area_type,
                    current_count=flow_data[area_type],
                    max_capacity=max_capacity[area_type],
                    timestamp=now,
                )
                session.add(flow)

        # 提交資料庫變更
        await session.commit()
