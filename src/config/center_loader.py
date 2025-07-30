"""
運動中心配置讀取器
負責從 YAML 檔案讀取運動中心配置
"""

import yaml
from typing import Dict, Any, Optional
from pathlib import Path


class CenterLoader:
    def __init__(self):
        self.centers_config: Dict[str, Any] = {}
        self._load_configs()

    def _load_configs(self):
        """載入所有配置文件"""
        config_dir = Path(__file__).parent

        # 載入 web_scrapers.yaml
        web_scrapers_path = config_dir / "web_scrapers.yaml"
        if web_scrapers_path.exists():
            with open(web_scrapers_path, "r", encoding="utf-8") as f:
                web_scrapers = yaml.safe_load(f)
                if web_scrapers and "centers" in web_scrapers:
                    for center_id, center_info in web_scrapers["centers"].items():
                        if center_info.get("status", False):
                            self.centers_config[center_id] = center_info

        # 載入 api_clients.yaml
        api_clients_path = config_dir / "api_clients.yaml"
        if api_clients_path.exists():
            with open(api_clients_path, "r", encoding="utf-8") as f:
                api_clients = yaml.safe_load(f)
                if api_clients and "centers" in api_clients:
                    for center_id, center_info in api_clients["centers"].items():
                        if center_info.get("status", False):
                            self.centers_config[center_id] = center_info

    def get_all_centers(self) -> Dict[str, Any]:
        """取得所有運動中心配置"""
        return self.centers_config

    def get_center_by_zip(self, zip_code: str) -> Optional[Dict[str, Any]]:
        """根據郵遞區號取得運動中心配置"""
        for center_id, center_info in self.centers_config.items():
            if center_info["basic_info"]["zip_code"] == zip_code:
                return {center_id: center_info}
        return None

    def get_center_ids_by_zip(self, zip_code: str) -> list[str]:
        """根據郵遞區號取得運動中心 ID 列表"""
        return [
            center_id
            for center_id, center_info in self.centers_config.items()
            if center_info["basic_info"]["zip_code"] == zip_code
        ]

    def get_center_facility_info(self, center_id: str) -> Optional[Dict[str, Any]]:
        """取得運動中心設施資訊"""
        if center_id in self.centers_config:
            return self.centers_config[center_id]["facility_info"]
        return None
