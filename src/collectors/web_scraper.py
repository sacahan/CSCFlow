from .base import FlowCollector
from bs4 import BeautifulSoup
import aiohttp
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


# WebScraperCollector 是專門用於網頁爬取的收集器類別。
# 它使用配置中的 URL 和選擇器來爬取並解析網頁資料。
class WebScraperCollector(FlowCollector):
    # 初始化 WebScraperCollector，接收配置字典並提取必要的參數。
    # config 包含目標 URL 和選擇器，用於指定要提取的資料。
    def __init__(self, config: Dict[str, Any]):
        self.url = config["url"]  # 目標網頁的 URL。
        self.selectors = config["selectors"]  # 用於提取資料的 CSS 選擇器。

    # collect_flow_data 方法負責發送 HTTP 請求並處理回應。
    # 它使用 aiohttp 庫進行非同步 HTTP 請求。
    async def collect_flow_data(self) -> Dict[str, Any]:
        try:
            async with aiohttp.ClientSession() as session:
                # 發送 GET 請求到指定的 URL。
                async with session.get(self.url) as response:
                    # 如果回應狀態碼不是 200，記錄錯誤並返回空字典。
                    if response.status != 200:
                        logger.error(f"HTTP錯誤 {response.status}: {self.url}")
                        return {}
                    # 解析回應的 HTML 內容並進行資料提取。
                    html = await response.text()
                    return await self._parse_html(html)
        except Exception as e:
            # 捕捉任何異常並記錄錯誤，返回空字典。
            logger.error(f"收集資料失敗 {self.url}: {str(e)}")
            return {}

    # _parse_html 方法解析 HTML 並提取所需的資料。
    # 它使用 BeautifulSoup 庫進行 HTML 解析。
    async def _parse_html(self, html: str) -> Dict[str, Any]:
        soup = BeautifulSoup(html, "html.parser")  # 初始化 BeautifulSoup 解析器。
        result = {}
        for area, config in self.selectors.items():
            try:
                # 使用 CSS 選擇器提取指定的 HTML 元素。
                element = soup.select_one(config["selector"])
                if element:
                    # 提取元素的文字內容並進行必要的轉換。
                    value = element.text.strip()
                    if config.get("transform") == "parseInt":
                        value = int(value)
                    result[area] = value
            except Exception as e:
                # 如果資料提取失敗，記錄錯誤並跳過該區域。
                logger.error(f"解析HTML失敗 {area}: {str(e)}")
        return result

    # validate_response 方法檢查回應資料是否符合預期格式。
    # 它確保所有必需的欄位都存在且類型正確。
    def validate_response(self, data: Dict[str, Any]) -> bool:
        return all(
            isinstance(data.get(area), (int, float))
            for area in ["gym", "pool"]  # 檢查特定區域的資料。
            if area in data
        )
