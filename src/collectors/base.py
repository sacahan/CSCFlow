from abc import ABC, abstractmethod
from typing import Dict, Any
from enum import Enum


# FlowCollector 是所有收集器的基底類別，提供通用功能和抽象方法。
# CollectorType 枚舉用於標識不同的收集器類型，例如網頁爬取和 API 客戶端。
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
