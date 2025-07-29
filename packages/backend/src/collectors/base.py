from abc import ABC, abstractmethod
from typing import Dict, Any
from enum import Enum


class CollectorType(str, Enum):
    WEB_SCRAPER = "web_scraper"
    API_CLIENT = "api_client"


class FlowCollector(ABC):
    @abstractmethod
    async def collect_flow_data(self) -> Dict[str, Any]:
        """收集流量資料"""
        pass

    @abstractmethod
    def validate_response(self, data: Dict[str, Any]) -> bool:
        """驗證回應資料"""
        pass
