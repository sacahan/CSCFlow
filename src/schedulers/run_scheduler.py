import asyncio
import logging
import sys
import os

from src.schedulers.flow_task import FlowTask
from src.schedulers.trend_task import TrendTask

# 設定 Python 路徑以便能夠引入專案模組
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("scheduler.log")],
)
logger = logging.getLogger(__name__)


async def run_scheduler_once(task_type: str = "all"):
    """
    執行一次性的排程任務，用於除錯

    Args:
        task_type (str): 要執行的任務類型，可選值為 "all"、"flow" 或 "trend"
    """
    try:
        logger.info(f"正在執行一次性排程任務 ({task_type})...")

        if task_type in ["all", "flow"]:
            flow_task = FlowTask()
            await flow_task.run_once()  # 立即執行一次流量收集

        if task_type in ["all", "trend"]:
            trend_task = TrendTask()
            await trend_task.run_once()  # 立即執行一次趨勢統計

        logger.info("一次性排程任務執行完成")
    except Exception as e:
        logger.error(f"執行一次性排程任務時發生錯誤: {str(e)}")
        raise


async def start_schedulers(task_type: str = "all"):
    """
    啟動定時排程作業

    Args:
        task_type (str): 要啟動的排程類型，可選值為 "all"、"flow" 或 "trend"
    """
    flow_task = None
    trend_task = None
    try:
        logger.info(f"正在啟動定時排程作業 ({task_type})...")

        if task_type in ["all", "flow"]:
            flow_task = FlowTask()
            await flow_task.start()  # 啟動流量收集排程

        if task_type in ["all", "trend"]:
            trend_task = TrendTask()
            await trend_task.start()  # 啟動趨勢統計排程

        # 保持程式運行，並監聽 Ctrl+C 中斷事件
        while True:
            try:
                await asyncio.sleep(60)
            except (KeyboardInterrupt, asyncio.exceptions.CancelledError):
                break
    except Exception as e:
        logger.error(f"執行定時排程作業時發生錯誤: {str(e)}")
        raise
    finally:
        # 確保資源清理
        if flow_task and task_type in ["all", "flow"]:
            await flow_task.shutdown()
        if trend_task and task_type in ["all", "trend"]:
            await trend_task.shutdown()
        logger.info("定時排程作業已停止")


async def main(mode: str = "run"):
    """
    主要執行函數
    根據模式選擇執行一次性任務或啟動定時排程

    Args:
        mode (str): 執行模式，可選值為:
            排程模式:
            - "run": 啟動所有排程 (預設)
            - "flow": 只啟動流量收集排程
            - "trend": 只啟動趨勢統計排程
            一次性執行:
            - "once": 執行所有一次性任務
            - "once-f": 只執行一次流量收集
            - "once-t": 只執行一次趨勢統計
    """
    try:
        if mode.startswith("once"):
            # 處理一次性執行模式
            task_type = {"once": "all", "once-f": "flow", "once-t": "trend"}.get(
                mode, "all"
            )
            await run_scheduler_once(task_type)
        else:
            # 處理排程模式
            task_type = "all" if mode == "run" else mode
            await start_schedulers(task_type)
    except Exception as e:
        logger.error(f"執行時發生錯誤: {str(e)}")
        raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, asyncio.exceptions.CancelledError):
        # 合併處理兩種中斷情況
        logger.info("程式執行被中斷，正在清理資源...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"程式執行失敗: {str(e)}")
        sys.exit(1)
