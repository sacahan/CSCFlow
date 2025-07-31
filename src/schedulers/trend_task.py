import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from sqlalchemy import func, and_
import logging
from ..database.models import RealTimeFlow, HistoricalStats
from ..database.db import AsyncSessionLocal

logger = logging.getLogger(__name__)


class TrendTask:
    def __init__(self):
        """初始化 TrendTask 類別，建立非同步排程器"""
        self.scheduler = AsyncIOScheduler()

    async def start(self):
        """
        啟動排程器並新增統計資料計算的排程任務
        每天凌晨 1 點執行日統計
        每週一凌晨 2 點執行週統計
        每月 1 號凌晨 3 點執行月統計
        """
        try:
            # 新增日統計排程
            self.scheduler.add_job(
                self._calculate_daily_stats,
                CronTrigger(hour=1),
                id="daily_stats",
                replace_existing=True,
            )

            # 新增週統計排程
            self.scheduler.add_job(
                self._calculate_weekly_stats,
                CronTrigger(day_of_week=0, hour=2),  # 每週一凌晨2點
                id="weekly_stats",
                replace_existing=True,
            )

            # 新增月統計排程
            self.scheduler.add_job(
                self._calculate_monthly_stats,
                CronTrigger(day=1, hour=3),  # 每月1號凌晨3點
                id="monthly_stats",
                replace_existing=True,
            )

            self.scheduler.start()
            logger.info("趨勢統計排程已啟動")
        except Exception as e:
            logger.error(f"啟動統計排程失敗: {str(e)}")
            raise

    async def shutdown(self):
        """關閉排程器，停止所有排程任務"""
        try:
            self.scheduler.shutdown()
            logger.info("趨勢統計排程已關閉")
        except Exception as e:
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
            stats_type (str): 統計類型 (daily/weekly/monthly)
        """
        async with AsyncSessionLocal() as session:
            try:
                # 查詢指定時間區間的流量數據，按運動中心和區域類型分組
                query = (
                    session.query(
                        RealTimeFlow.zip_code,
                        RealTimeFlow.area_type,
                        func.count(RealTimeFlow.id).label("total_count"),
                        func.avg(RealTimeFlow.current_count).label("avg_count"),
                        func.max(RealTimeFlow.current_count).label("max_count"),
                        func.min(RealTimeFlow.current_count).label("min_count"),
                    )
                    .filter(
                        and_(
                            RealTimeFlow.timestamp >= start_date,
                            RealTimeFlow.timestamp <= end_date,
                        )
                    )
                    .group_by(RealTimeFlow.zip_code, RealTimeFlow.area_type)
                )

                results = await session.execute(query)

                # 儲存統計結果
                for result in results:
                    stat = HistoricalStats(
                        zip_code=result.zip_code,
                        area_type=result.area_type,
                        stats_type=stats_type,
                        start_date=start_date.date(),
                        end_date=end_date.date(),
                        total_count=result.total_count,
                        avg_count=float(result.avg_count),
                        max_count=result.max_count,
                        min_count=result.min_count,
                    )
                    session.add(stat)

                await session.commit()
                logger.info(f"{stats_type.capitalize()} 統計完成")

            except Exception as e:
                await session.rollback()
                logger.error(f"計算 {stats_type} 統計失敗: {str(e)}")
                raise

    async def _calculate_daily_stats(self):
        """計算昨日統計數據"""
        yesterday = datetime.now() - timedelta(days=1)
        start_date = datetime(yesterday.year, yesterday.month, yesterday.day)
        end_date = start_date + timedelta(days=1)
        await self._calculate_stats(start_date, end_date, "daily")

    async def _calculate_weekly_stats(self):
        """計算上週統計數據"""
        today = datetime.now()
        # 計算上週一的日期
        last_week_start = today - timedelta(days=today.weekday() + 7)
        start_date = datetime(
            last_week_start.year, last_week_start.month, last_week_start.day
        )
        end_date = start_date + timedelta(days=7)
        await self._calculate_stats(start_date, end_date, "weekly")

    async def _calculate_monthly_stats(self):
        """計算上月統計數據"""
        today = datetime.now()
        if today.month == 1:
            last_month_year = today.year - 1
            last_month = 12
        else:
            last_month_year = today.year
            last_month = today.month - 1

        start_date = datetime(last_month_year, last_month, 1)
        if last_month == 12:
            end_date = datetime(last_month_year + 1, 1, 1)
        else:
            end_date = datetime(last_month_year, last_month + 1, 1)

        await self._calculate_stats(start_date, end_date, "monthly")

    async def run_once(self):
        """立即執行一次所有統計任務，方便調試"""

        start_time = time.time()
        try:
            await self._calculate_daily_stats()
            await self._calculate_weekly_stats()
            await self._calculate_monthly_stats()
            logger.info("完成所有統計任務")
        except Exception as e:
            logger.error(f"立即執行統計任務失敗: {str(e)}")
            raise

        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"趨勢統計排程完成，總耗時: {execution_time:.2f} 秒")
