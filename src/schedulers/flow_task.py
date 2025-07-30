from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import logging
import time
from ..database.models import RealTimeFlow
from ..collectors.factory import CollectorFactory
from ..database.db import AsyncSessionLocal
from ..config.center_loader import CenterLoader

logger = logging.getLogger(__name__)


class FlowTask:
    def __init__(self):
        """初始化 FlowTask 類別，建立非同步排程器和中心載入器"""
        self.scheduler = AsyncIOScheduler()
        self.center_loader = CenterLoader()

    async def start(self):
        """
        啟動排程器並新增收集流量資料的排程任務。
        排程任務每 5 分鐘執行一次。
        """
        try:
            self.scheduler.add_job(
                self._collect_all_centers_flow,
                CronTrigger(minute="*/5"),  # 每5分鐘執行
                id="collect_flow_data",
                replace_existing=True,
            )
            self.scheduler.start()
            logger.info("流量收集排程已啟動")
        except Exception as e:
            logger.error(f"啟動排程失敗: {str(e)}")
            raise

    async def shutdown(self):
        """
        關閉排程器，停止所有排程任務。
        """
        try:
            self.scheduler.shutdown()
            logger.info("流量收集排程已關閉")
        except Exception as e:
            logger.error(f"關閉排程失敗: {str(e)}")
            raise

    async def _collect_all_centers_flow(self):
        """
        收集所有運動中心的即時流量資料。
        使用 CenterLoader 讀取配置並透過 CollectorFactory 建立資料收集器。
        """
        start_time = time.time()
        centers = self.center_loader.get_all_centers()
        logger.info(f"開始收集 {len(centers)} 個運動中心的資料")

        async with AsyncSessionLocal() as session:
            for center_id, center_info in centers.items():
                if not center_info.get("status", False):
                    continue

                try:
                    collector_config = center_info.get("collector", {})
                    collector_type = collector_config.get("type")
                    config = collector_config.get("config", {})

                    # 根據運動中心的收集器類型與設定建立資料收集器: api_client 或 web_scraper
                    collector = CollectorFactory.create_collector(
                        collector_type, config
                    )

                    # 收集即時流量資料
                    flow_data = await collector.collect_flow_data()

                    # 驗證收集到的資料是否正確
                    if collector.validate_response(flow_data):
                        zip_code = center_info["basic_info"]["zip_code"]
                        await self._save_flow_data(session, zip_code, flow_data)
                        logger.info(
                            f"✅ 成功收集資料 - {center_info['basic_info']['name']}"
                        )
                    else:
                        logger.error(
                            f"❌ 資料驗證失敗 - {center_info['basic_info']['name']}"
                        )

                except Exception as e:
                    # 捕捉例外並記錄錯誤訊息
                    logger.error(
                        f"收集資料失敗 - {center_info['basic_info']['name']}: {str(e)}"
                    )
                    continue

        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"所有運動中心的流量資料收集完成，總耗時: {execution_time:.2f} 秒")

    async def _save_flow_data(
        self,
        session,
        zip_code: str,
        flow_data: dict,
    ):
        """
        將收集到的流量資料儲存到資料庫中。

        :param session: 非同步資料庫會話
        :param zip_code: 運動中心的郵遞區號
        :param flow_data: 收集到的流量資料: {gym: int, pool: int}
        """
        now = datetime.now()

        # 準備要儲存的流量資料
        for area, flow in flow_data.items():
            flow = RealTimeFlow(
                zip_code=zip_code,
                area_type=area,
                current_count=flow,
                timestamp=now,
            )
            session.add(flow)

        # 提交資料庫變更
        await session.commit()

    async def run_once(self):
        """
        立即執行一次流量收集任務，方便調試。
        """
        try:
            await self._collect_all_centers_flow()
            logger.info("流量收集任務已執行完畢")
        except Exception as e:
            logger.error(f"立即執行流量收集任務失敗: {str(e)}")
            raise
