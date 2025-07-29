from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from ..services.flow_service import FlowService

logger = logging.getLogger(__name__)


class JobScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.flow_service = FlowService()

    async def start(self):
        """啟動所有排程任務"""
        # 流量收集任務
        self.scheduler.add_job(
            self.flow_service.collect_all_centers_flow,
            CronTrigger(minute="*/5"),
            id="collect_flow_data",
            replace_existing=True,
        )

        # 可以在這裡添加其他排程任務

        self.scheduler.start()
        logger.info("所有排程任務已啟動")

    async def shutdown(self):
        """關閉排程器"""
        self.scheduler.shutdown()
        logger.info("所有排程任務已關閉")
