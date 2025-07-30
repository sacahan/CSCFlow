import asyncio
import logging
import sys
import os

# 設定 Python 路徑以便能夠引入專案模組
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from .flow_task import FlowTask

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("scheduler.log")],
)
logger = logging.getLogger(__name__)


async def main():
    """
    主要執行函數
    初始化並執行 FlowTask
    """
    try:
        logger.info("正在初始化流量收集排程...")
        flow_task = FlowTask()
        await flow_task.run_once()
    except Exception as e:
        logger.error(f"執行時發生錯誤: {str(e)}")
        raise
    finally:
        logger.info("程式已終止")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass  # 優雅地處理 Ctrl+C
    except Exception as e:
        logger.error(f"程式執行失敗: {str(e)}")
        sys.exit(1)
