from .base import FlowCollector
import aiohttp
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


# ApiCollector 是專門用於 API 資料收集的收集器類別。
# 它使用配置中的端點、方法和標頭來呼叫 API 並處理回應。
# collect_flow_data 方法負責發送 API 請求並處理回應。
# _map_response 方法將回應資料映射到指定的格式。
# validate_response 方法檢查回應資料是否符合預期格式。
class ApiCollector(FlowCollector):
    def __init__(self, config: Dict[str, Any]):
        self.endpoint = config["endpoint"]
        self.method = config["method"]
        self.headers = config.get("headers", {})
        self.response_mapping = config["response_mapping"]

    async def collect_flow_data(self) -> Dict[str, Any]:
        try:
            async with aiohttp.ClientSession() as session:
                request = getattr(session, self.method.lower())
                async with request(self.endpoint, headers=self.headers) as response:
                    if response.status != 200:
                        logger.error(f"API錯誤 {response.status}: {self.endpoint}")
                        return {}
                    data = await response.json()
                    return self._map_response(data)
        except Exception as e:
            logger.error(f"API呼叫失敗 {self.endpoint}: {str(e)}")
            return {}

    def _map_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = {}
        for key, mapping in self.response_mapping.items():
            try:
                value = data
                for path in mapping["path"].split("."):
                    value = value[path]
                if isinstance(value, str):
                    value = int(value)
                result[key] = value
            except Exception as e:
                logger.error(f"回應資料轉換失敗 {key}: {str(e)}")
        return result

    def validate_response(self, data: Dict[str, Any]) -> bool:
        required_fields = self.response_mapping.keys()
        return all(
            isinstance(data.get(field), (int, float)) for field in required_fields
        )
