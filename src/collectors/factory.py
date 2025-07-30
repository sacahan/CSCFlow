from .base import FlowCollector, CollectorType  # 匯入基底收集器類別和收集器類型枚舉
from .web_scraper import WebScraperCollector  # 匯入網頁爬取收集器類別
from .api_client import ApiCollector  # 匯入 API 客戶端收集器類別


# CollectorFactory 是用於創建收集器實例的工廠類別。
# create_collector 方法根據收集器類型和配置創建具體的收集器。
# 它支援 WebScraperCollector 和 ApiCollector 類型。
# 如果提供的收集器類型無效，則拋出 ValueError。
class CollectorFactory:
    """
    收集器工廠類別，用於根據指定的收集器類型創建相應的收集器實例。
    """

    @staticmethod
    def create_collector(collector_type: str, config: dict) -> FlowCollector:
        """
        根據收集器類型和配置創建收集器實例。

        :param collector_type: 收集器類型，應為 CollectorType 枚舉中的值。
        :param config: 配置字典，包含初始化收集器所需的參數。
        :return: FlowCollector 的具體實例。
        :raises ValueError: 如果提供的收集器類型無效，則拋出此例外。
        """
        if collector_type == CollectorType.WEB_SCRAPER:
            # 如果收集器類型是網頁爬取，返回 WebScraperCollector 的實例
            return WebScraperCollector(config)
        elif collector_type == CollectorType.API_CLIENT:
            # 如果收集器類型是 API 客戶端，返回 ApiCollector 的實例
            return ApiCollector(config)
        # 如果收集器類型無效，拋出 ValueError 並提供錯誤訊息
        raise ValueError(f"未知的收集器類型: {collector_type}")
