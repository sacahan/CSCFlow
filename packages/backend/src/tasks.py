from datetime import datetime, timedelta
from sqlalchemy import func
from .models import RealTimeFlow, HistoricalStats
from .db import get_db
from fastapi import FastAPI
import logging
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)


async def calculate_hourly_stats():
    """計算每小時的統計數據"""
    db = next(get_db())
    try:
        # 取得一小時前的時間點
        hour_ago = datetime.now(datetime.timezone.utc) - timedelta(hours=1)

        # 查詢每個運動中心各區域的統計數據
        stats = (
            db.query(
                func.avg(RealTimeFlow.current_count).label("avg_count"),
                func.max(RealTimeFlow.current_count).label("max_count"),
                RealTimeFlow.center_id,
                RealTimeFlow.area_type,
            )
            .filter(RealTimeFlow.timestamp >= hour_ago)
            .group_by(RealTimeFlow.center_id, RealTimeFlow.area_type)
            .all()
        )

        # 更新或插入統計數據
        for stat in stats:
            db.merge(
                HistoricalStats(
                    center_id=stat.center_id,
                    area_type=stat.area_type,
                    avg_count=stat.avg_count,
                    max_count=stat.max_count,
                    date=datetime.now(datetime.timezone.utc).date(),
                )
            )
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


async def cleanup_old_data():
    """清理超過30天的即時數據"""
    db = next(get_db())
    try:
        thirty_days_ago = datetime.now(datetime.timezone.utc) - timedelta(days=30)
        db.query(RealTimeFlow).filter(RealTimeFlow.timestamp < thirty_days_ago).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def init_scheduled_tasks(app: FastAPI):
    """初始化定時任務"""

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        async def hourly_stats_task():
            try:
                await calculate_hourly_stats()
            except Exception as e:
                logger.error(f"計算統計數據時發生錯誤: {e}")

        async def daily_cleanup_task():
            try:
                await cleanup_old_data()
            except Exception as e:
                logger.error(f"清理舊數據時發生錯誤: {e}")

        app.state.hourly_stats_task = hourly_stats_task
        app.state.daily_cleanup_task = daily_cleanup_task

        yield

        # Cleanup logic if needed
        del app.state.hourly_stats_task
        del app.state.daily_cleanup_task

    app.router.lifespan_context = lifespan

    async def daily_cleanup_task():
        try:
            await cleanup_old_data()
        except Exception as e:
            logger.error(f"清理舊數據時發生錯誤: {e}")

    app.state.daily_cleanup_task = daily_cleanup_task
