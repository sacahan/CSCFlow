from pathlib import Path
import yaml
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class ConfigLoader:
    def __init__(self, config_dir: str = None):
        if config_dir is None:
            config_dir = str(Path(__file__).parent)
        self.config_dir = Path(config_dir)

    def load_collectors_config(self) -> Dict[str, Any]:
        """載入所有收集器配置"""
        config = {"centers": {}}

        # 載入 API 客戶端配置
        api_config = self._load_yaml("api_clients.yaml")
        if api_config and "centers" in api_config:
            config["centers"].update(api_config["centers"])

        # 載入網頁爬蟲配置
        web_config = self._load_yaml("web_scrapers.yaml")
        if web_config and "centers" in web_config:
            config["centers"].update(web_config["centers"])

        # 全域設定使用任一配置檔的設定
        if api_config and "global_settings" in api_config:
            config["global_settings"] = api_config["global_settings"]
        elif web_config and "global_settings" in web_config:
            config["global_settings"] = web_config["global_settings"]

        return config

    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        """載入 YAML 檔案"""
        try:
            file_path = self.config_dir / filename
            if not file_path.exists():
                logger.warning(f"找不到配置檔案: {file_path}")
                return None

            with open(file_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"載入配置檔案失敗 {filename}: {str(e)}")
            return None
