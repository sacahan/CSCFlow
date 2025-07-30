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
    def __init__(self, configs: list[Dict[str, Any]]):
        self.configs = configs  # 配置列表，包含多個 API 呼叫的設定。

    # collect_flow_data 方法負責發送 API 請求並處理回應。
    # 它使用 aiohttp 庫進行非同步 HTTP 請求。
    async def collect_flow_data(self) -> Dict[str, Any]:
        results = {}

        try:
            async with aiohttp.ClientSession() as session:
                for config in self.configs:
                    endpoint = config.get("endpoint")
                    method = config.get("method", "GET").upper()
                    headers = config.get(
                        "headers", {"Content-Type": "application/json"}
                    )
                    response_format = config.get("response_format", "json")
                    mapping_path = config.get("mapping_path", {})

                    # 根據配置的 HTTP 方法動態調用相應的請求方法。
                    request = getattr(session, method.lower())

                    logger.info(f"🚀 Calling API: {endpoint} with method {method}")
                    async with request(endpoint, headers=headers) as response:
                        # 如果回應狀態碼不是 200，記錄錯誤並返回空字典。
                        if response.status != 200:
                            logger.error(f"API錯誤 {response.status}: {endpoint}")
                            return {}

                        # 先取回純文字內容
                        data = await response.text()

                        # Mapping 格式以取得所需的資料。
                        parsed = self._map_response(data, response_format, mapping_path)

                        # 加入結果到總結果字典中。
                        results.update(parsed)

                logger.info(f"📊 收集到的資料: {results}")
                return results

        except Exception as e:
            # 捕捉任何異常並記錄錯誤，返回空字典。
            logger.error(f"API呼叫失敗 {self.configs[0]['endpoint']}: {str(e)}")
            return {}

    # _map_response 方法將回應資料映射到指定的格式。
    # 它根據配置的映射規則提取並轉換回應中的資料。
    def _map_response(
        self, data: Any, format: str, mappings: Dict[str, Any]
    ) -> Dict[str, Any]:
        result = {}

        if format == "json":
            try:
                # 嘗試將回應資料解析為 JSON 格式。
                data = json.loads(data)
            except json.JSONDecodeError:
                raise ValueError(f"無效的 JSON 格式: '{data}'")
        elif format == "comma":
            # 如果格式是逗號分隔，將資料分割成列表。
            data = data.split(",")

        for area, paths in mappings.items():
            try:
                value = data
                # 根據映射規則的路徑逐層提取資料。
                for path in paths.split("."):
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

                # 轉換為整數並存入結果字典。
                result[area] = int(value)
            except Exception as e:
                raise ValueError(f"無法從回應資料中提取 '{area}' 的值: {str(e)}")
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
