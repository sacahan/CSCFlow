import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from sqlalchemy import func, and_, Integer
import logging
from ..database.models import RealTimeFlow, HistoricalStats
from ..database.db import AsyncSessionLocal
from sqlalchemy.sql import select
from sqlalchemy.dialects.postgresql import insert

# 設定 logger 用於記錄排程器的執行狀態
logger = logging.getLogger(__name__)


class TrendTask:
    def __init__(self):
        """初始化 TrendTask 類別，建立非同步排程器"""
        self.scheduler = AsyncIOScheduler()

    async def start(self):
        """
        啟動排程器並新增統計資料計算的排程任務
        每天晚上 11 點執行每日統計
        每小時執行每小時統計
        """
        try:
            # 新增日統計排程，設定每天晚上 11 點執行
            self.scheduler.add_job(
                self._calculate_daily_stats,
                CronTrigger(hour=23),
                id="daily_stats",
                replace_existing=True,
            )

            # 新增每小時統計排程，設定每小時執行
            self.scheduler.add_job(
                self._calculate_hourly_stats,
                CronTrigger(minute=0, hour="9-21"),
                id="hourly_stats",
                replace_existing=True,
            )

            # 啟動排程器
            self.scheduler.start()
            logger.info("趨勢統計排程已啟動")
        except Exception as e:
            # 捕捉啟動失敗的例外並記錄錯誤訊息
            logger.error(f"啟動統計排程失敗: {str(e)}")
            raise

    async def shutdown(self):
        """關閉排程器，停止所有排程任務"""
        try:
            # 關閉排程器並記錄狀態
            self.scheduler.shutdown()
            logger.info("趨勢統計排程已關閉")
        except Exception as e:
            # 捕捉關閉失敗的例外並記錄錯誤訊息
            logger.error(f"關閉統計排程失敗: {str(e)}")
            raise

    async def _calculate_stats(
        self, start_date: datetime, end_date: datetime, stats_type: str
    ):
        """
        計算指定時間區間的統計數據

        Args:
            start_date (datetime): 統計開始日期
            end_date (datetime): 統計結束日期
            stats_type (str): 統計類型 (daily/hourly)
        """
        async with AsyncSessionLocal() as session:
            try:
                # 查詢指定時間區間的流量數據，按運動中心和區域類型分組
                query = (
                    select(
                        RealTimeFlow.zip_code,
                        RealTimeFlow.area_type,
                        func.cast(func.avg(RealTimeFlow.current_count), Integer).label(
                            "avg_count"
                        ),
                        func.max(RealTimeFlow.current_count).label("max_count"),
                        func.min(RealTimeFlow.current_count).label("min_count"),
                    )
                    .where(
                        and_(
                            RealTimeFlow.timestamp >= start_date,
                            RealTimeFlow.timestamp <= end_date,
                        )
                    )
                    .group_by(RealTimeFlow.zip_code, RealTimeFlow.area_type)
                )

                # 執行查詢並獲取結果
                results = await session.execute(query)

                # 儲存統計結果到 HistoricalStats 表
                for result in results:
                    insert_stmt = (
                        insert(HistoricalStats)
                        .values(
                            zip_code=result.zip_code,
                            area_type=result.area_type,
                            stats_type=stats_type,
                            start_date=start_date,  # 使用 DateTime 型別
                            end_date=end_date,  # 使用 DateTime 型別
                            avg_count=float(result.avg_count),
                            max_count=result.max_count,
                            min_count=result.min_count,
                        )
                        .on_conflict_do_update(
                            constraint="unique_stats_constraint",
                            set_={
                                "avg_count": float(result.avg_count),
                                "max_count": result.max_count,
                                "min_count": result.min_count,
                            },
                        )
                    )

                    await session.execute(insert_stmt)

                # 提交交易
                await session.commit()
                logger.info(f"{stats_type.capitalize()} 統計完成")

            except Exception as e:
                # 回滾交易並記錄錯誤訊息
                await session.rollback()
                logger.error(f"計算 {stats_type} 統計失敗: {str(e)}")
                raise

    async def _calculate_daily_stats(self):
        """計算昨日統計數據"""
        yesterday = datetime.now() - timedelta(days=1)
        start_date = datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0)
        end_date = datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59, 59)
        await self._calculate_stats(start_date, end_date, "daily")

    async def _calculate_hourly_stats(self):
        """計算前一小時統計數據"""
        current_time = datetime.now() - timedelta(hours=1)
        print(f"Current hour: {current_time.hour}")
        start_date = datetime(
            current_time.year,
            current_time.month,
            current_time.day,
            current_time.hour,
            0,
            0,
        )
        end_date = datetime(
            current_time.year,
            current_time.month,
            current_time.day,
            current_time.hour,
            59,
            59,
        )
        await self._calculate_stats(start_date, end_date, "hourly")

    async def run_once(self):
        """立即執行一次每小時與每日統計任務，方便調試"""

        logger.info("=== 執行每小時與每日統計任務 ===")
        start_time = time.time()
        try:
            # 順序執行每小時與每日統計任務
            await self._calculate_hourly_stats()
            await self._calculate_daily_stats()
        except Exception as e:
            # 捕捉例外並記錄錯誤訊息
            logger.error(f"立即執行統計任務失敗: {str(e)}")
            raise

        end_time = time.time()
        execution_time = end_time - start_time
        # 記錄執行耗時
        logger.info(f"=== 趨勢統計排程完成，總耗時: {execution_time:.2f} 秒 ===")
