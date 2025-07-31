from .base import FlowCollector
import aiohttp
from typing import Dict, Any
import logging
from lxml import html
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)


# WebScraperCollector 是專門用於網頁爬取的收集器類別。
# 它使用配置中的 URL 和選擇器來爬取並解析網頁資料。
class WebScraperCollector(FlowCollector):
    # 初始化 WebScraperCollector，接收配置字典並提取必要的參數。
    # config 包含目標 URL 和選擇器，用於指定要提取的資料。
    def __init__(self, configs: list[Dict[str, Any]]):
        self.url = configs[0]["url"]  # 目標網頁的 URL。
        self.xpath_selectors = configs[0][
            "xpath_selectors"
        ]  # 用於提取資料的 CSS 選擇器。
        # 是否需要使用Playwright來渲染JavaScript
        self.use_playwright = configs[0].get("use_playwright", False)

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
                    # 先取回純文字內容
                    html = await response.text()
                    # print(f"{html}")
                    # 解析回應的 HTML 內容並進行資料提取。
                    results = await self._parse_html(html)

                    logger.info(f"📊 收集到的資料: {results} ({self.url})")
                    return results
        except Exception as e:
            # 捕捉任何異常並記錄錯誤，返回空字典。
            logger.error(f"收集資料失敗 {self.url}: {str(e)}")
            return {}

    # _parse_html 方法解析 HTML 並提取所需的資料。
    # 它可以使用 lxml 進行靜態解析，或使用 Playwright 處理動態渲染的內容。
    async def _parse_html(self, html_content: str) -> Dict[str, Any]:
        result = {}

        if self.use_playwright:
            # 使用 Playwright 處理動態渲染的內容
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                try:
                    # 將HTML內容注入到新頁面
                    await page.set_content(html_content)
                    # 等待頁面完全載入
                    await page.wait_for_load_state("networkidle")

                    for area, xpath in self.xpath_selectors.items():
                        try:
                            # 使用 xpath= 前綴指定選擇器類型
                            element = await page.wait_for_selector(
                                f"xpath={xpath}", state="attached"
                            )
                            if element:
                                value = await element.text_content()
                                value = value.strip() if value else "0"

                                # 轉換值為整數
                                if value == "" or value is None:
                                    value = 0
                                else:
                                    try:
                                        value = int(value)
                                    except ValueError:
                                        value = 0

                                result[area] = value
                            else:
                                raise ValueError(
                                    f"使用Playwright未找到元素 {area} 使用的選擇器: {xpath}"
                                )

                        except Exception as e:
                            logger.error(f"使用Playwright解析失敗 {area}: {str(e)}")

                finally:
                    await browser.close()
        else:
            # 使用lxml進行靜態HTML解析
            tree = html.fromstring(html_content)
            for area, xpath in self.xpath_selectors.items():
                try:
                    elements = tree.xpath(xpath)
                    if elements and len(elements) > 0:
                        value = elements[0].strip()
                        if value == "" or value is None:
                            value = 0
                        else:
                            try:
                                value = int(value)
                            except ValueError:
                                value = 0

                        result[area] = value
                    else:
                        raise ValueError(f"未找到元素 {area} 使用的 XPath: {xpath}")

                except Exception as e:
                    logger.error(f"解析HTML失敗 {area}: {str(e)}")

        return result

    # validate_response 方法檢查回應資料是否符合預期格式。
    # 它確保所有必需的欄位都存在且類型正確。
    def validate_response(self, data: Dict[str, Any]) -> bool:
        # 檢核 data 中的 gym 和 pool 是否存在且類型正確。
        if ("gym" in data and isinstance(data["gym"], int)) or (
            "pool" in data and isinstance(data["pool"], int)
        ):
            return True
        else:
            logger.error("回應資料驗證失敗: 缺少或類型錯誤的欄位")
            return False
