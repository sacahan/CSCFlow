from .base import FlowCollector
import aiohttp
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


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
