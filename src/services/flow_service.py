"""
流量服務
處理運動中心人流相關的業務邏輯
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from ..database.repositories import RealTimeFlowRepository
from ..config.center_loader import CenterLoader

logger = logging.getLogger(__name__)


# FlowService 類別負責處理運動中心人流相關的業務邏輯
class FlowService:
    def __init__(self, session: AsyncSession):
        # 初始化 FlowService
        self.session = session
        self.flow_repository = RealTimeFlowRepository(session)
        self.center_loader = CenterLoader()

    def get_all_centers(self) -> List[Dict[str, Any]]:
        """取得所有運動中心列表"""

        centers_config = self.center_loader.get_all_centers()
        return [
            {
                "name": center_info["basic_info"]["name"],
                "zip_code": center_info["basic_info"]["zip_code"],
                "address": center_info["basic_info"]["address"],
                "website_url": center_info["basic_info"]["website_url"],
                "facility_info": center_info["facility_info"],
            }
            for center_info in centers_config.values()
        ]

    def get_center_detail_by_zip(self, zip_code: str) -> Optional[Dict[str, Any]]:
        """取得特定運動中心詳情"""
        center = self.center_loader.get_center_by_zip(zip_code)
        if not center:
            return None

        center_id, center_info = next(iter(center.items()))
        return {
            "name": center_info["basic_info"]["name"],
            "zip_code": center_info["basic_info"]["zip_code"],
            "address": center_info["basic_info"]["address"],
            "website_url": center_info["basic_info"]["website_url"],
            "facility_info": center_info["facility_info"],
        }

    async def get_current_flows(self, zip_code: str) -> Dict[str, Any]:
        """取得即時人流數據"""
        # 取得運動中心資訊
        center = self.center_loader.get_center_by_zip(zip_code)
        if not center:
            return {"timestamp": datetime.now(), "centers": []}

        center_id, center_info = next(iter(center.items()))

        # 初始化運動中心的流量資料
        center_flow = {
            "zip_code": center_info["basic_info"]["zip_code"],
            "name": center_info["basic_info"]["name"],
            "gym": {
                "current_count": 0,
                "max_capacity": center_info["facility_info"]["gym"]["max_capacity"],
            },
            "pool": {
                "current_count": 0,
                "max_capacity": center_info["facility_info"]["pool"]["max_capacity"],
            },
        }

        # 取得最新流量資料，更新流量數據
        for area_type in ["gym", "pool"]:
            if center_info["facility_info"][area_type]["available"]:
                flow = await self.flow_repository.get_latest_flow(zip_code, area_type)
                if flow:
                    center_flow[area_type]["current_count"] = flow.current_count

        # 返回包含時間戳和運動中心流量資料的結果
        return {"timestamp": datetime.now(), "centers": [center_flow]}

    async def get_trend_stats(
        self, zip_code: str, area_type: str, time_range: str
    ) -> Dict[str, Any]:
        """取得趨勢統計資料"""
        # 根據 zip_code 取得運動中心資料，若不存在則返回 None
        center = self.center_loader.get_center_by_zip(zip_code)
        if not center:
            return None

        center_id, center_info = next(iter(center.items()))

        # 檢查設施是否可用
        if not center_info["facility_info"][area_type]["available"]:
            return None

        # 根據 time_range 計算時間範圍
        end_time = datetime.now()
        if time_range == "daily":
            start_time = end_time - timedelta(days=1)
        elif time_range == "weekly":
            start_time = end_time - timedelta(weeks=1)
        else:  # monthly
            start_time = end_time - timedelta(days=30)

        # 從 flow_repository 中取得指定時間範圍的流量資料
        flows = await self.flow_repository.get_flows_by_time_range(
            zip_code, area_type, start_time, end_time
        )

        # 格式化流量資料為時間戳與流量數據的列表
        data = [
            {"timestamp": flow.timestamp, "count": flow.current_count} for flow in flows
        ]

        return {
            "zip_code": zip_code,
            "area_type": area_type,
            "data": data,
            "max_capacity": center_info["facility_info"][area_type]["max_capacity"],
        }
