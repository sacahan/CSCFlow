from .base import FlowCollector, CollectorType
from .web_scraper import WebScraperCollector
from .api_client import ApiCollector


class CollectorFactory:
    @staticmethod
    def create_collector(collector_type: str, config: dict) -> FlowCollector:
        if collector_type == CollectorType.WEB_SCRAPER:
            return WebScraperCollector(config)
        elif collector_type == CollectorType.API_CLIENT:
            return ApiCollector(config)
        raise ValueError(f"未知的收集器類型: {collector_type}")
