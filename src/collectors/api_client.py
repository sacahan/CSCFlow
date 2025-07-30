from .base import FlowCollector
import aiohttp
from typing import Dict, Any
import logging
import json

logger = logging.getLogger(__name__)


# ApiCollector 是專門用於 API 資料收集的收集器類別。
# 它使用配置中的端點、方法和標頭來呼叫 API 並處理回應。
class ApiCollector(FlowCollector):
    # 初始化 ApiCollector，接收配置字典並提取必要的參數。
    # config 包含 API 的端點、HTTP 方法、標頭及回應映射。
    def __init__(self, config: Dict[str, Any]):
        self.endpoints = config["endpoints"]  # API 的端點 URL。
        self.method = config["method"]  # HTTP 方法，例如 GET 或 POST。
        self.headers = config.get("headers", {})  # 可選的 HTTP 標頭。
        self.response_mapping = config["response_mapping"]  # 回應資料的映射規則。

    # collect_flow_data 方法負責發送 API 請求並處理回應。
    # 它使用 aiohttp 庫進行非同步 HTTP 請求。
    async def collect_flow_data(self) -> Dict[str, Any]:
        try:
            async with aiohttp.ClientSession() as session:
                # 根據配置的 HTTP 方法動態調用相應的請求方法。
                request = getattr(session, self.method.lower())

                print(f"🚀 Calling API: {self.endpoints[0]} with method {self.method}")
                async with request(self.endpoints[0], headers=self.headers) as response:
                    # 如果回應狀態碼不是 200，記錄錯誤並返回空字典。
                    if response.status != 200:
                        logger.error(f"API錯誤 {response.status}: {self.endpoints[0]}")
                        return {}

                    # 根據回應的 Content-Type 判斷如何處理回應資料。
                    if response.headers.get("Content-Type", "").startswith("text/html"):
                        data = await response.text()
                        # 嘗試將 HTML 內容解析為 JSON。
                        try:
                            data = json.loads(data)
                        except (TypeError, ValueError, json.JSONDecodeError):
                            raise
                    else:
                        data = await response.json()
                    return self._map_response(data)
        except Exception as e:
            # 捕捉任何異常並記錄錯誤，返回空字典。
            logger.error(f"API呼叫失敗 {self.endpoints[0]}: {str(e)}")
            return {}

    # _map_response 方法將回應資料映射到指定的格式。
    # 它根據配置的映射規則提取並轉換回應中的資料。
    def _map_response(self, data: Any) -> Dict[str, Any]:
        result = {}

        for key, mapping in self.response_mapping.items():
            try:
                value = data
                # 根據映射規則的路徑逐層提取資料。
                for path in mapping["path"].split("."):
                    if isinstance(value, dict) and path in value:
                        value = value[path]
                    elif isinstance(value, list):
                        index = int(path)  # 假設 path 是有效的整數字串。
                        value = value[index]
                    else:
                        raise KeyError(f"Key '{path}' not found in the response data")

                # 如果空字串回傳0，如果提取的值是字串，嘗試將其轉換為整數。
                if value == "" or value is None:
                    value = 0
                elif isinstance(value, str) and mapping["type"] == "integer":
                    value = int(value)
                result[key] = value
            except Exception as e:
                logger.error(f"回應資料轉換失敗 {key}: {str(e)}")

        print(f"📊 收集到的資料: {result}")
        return result

    # validate_response 方法檢查回應資料是否符合預期格式。
    def validate_response(self, data: Dict[str, Any]) -> bool:
        # 檢核 data 中的 gym 和 pool 是否存在且類型正確。
        if ("gym" in data and isinstance(data["gym"], int)) or (
            "pool" in data and isinstance(data["pool"], int)
        ):
            return True
        else:
            logger.error("回應資料驗證失敗: 缺少或類型錯誤的欄位")
            return False
