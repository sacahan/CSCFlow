from .base import FlowCollector
from bs4 import BeautifulSoup
import aiohttp
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class WebScraperCollector(FlowCollector):
    def __init__(self, config: Dict[str, Any]):
        self.url = config["url"]
        self.selectors = config["selectors"]

    async def collect_flow_data(self) -> Dict[str, Any]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    if response.status != 200:
                        logger.error(f"HTTP錯誤 {response.status}: {self.url}")
                        return {}
                    html = await response.text()
                    return await self._parse_html(html)
        except Exception as e:
            logger.error(f"收集資料失敗 {self.url}: {str(e)}")
            return {}

    async def _parse_html(self, html: str) -> Dict[str, Any]:
        soup = BeautifulSoup(html, "html.parser")
        result = {}
        for area, config in self.selectors.items():
            try:
                element = soup.select_one(config["selector"])
                if element:
                    value = element.text.strip()
                    if config.get("transform") == "parseInt":
                        value = int(value)
                    result[area] = value
            except Exception as e:
                logger.error(f"解析HTML失敗 {area}: {str(e)}")
        return result

    def validate_response(self, data: Dict[str, Any]) -> bool:
        return all(
            isinstance(data.get(area), (int, float))
            for area in ["gym", "pool"]
            if area in data
        )
