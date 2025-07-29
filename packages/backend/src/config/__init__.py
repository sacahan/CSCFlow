from typing import Dict, Any
from .loader import ConfigLoader


class Settings:
    def __init__(self):
        self._config_loader = ConfigLoader()
        self._collectors_config = None

    @property
    def collectors_config(self) -> Dict[str, Any]:
        """取得收集器配置（懶載入）"""
        if self._collectors_config is None:
            self._collectors_config = self._config_loader.load_collectors_config()
        return self._collectors_config

    @property
    def global_settings(self) -> Dict[str, Any]:
        """取得全域設定"""
        return self.collectors_config.get("global_settings", {})

    @property
    def centers(self) -> Dict[str, Any]:
        """取得所有運動中心配置"""
        return self.collectors_config.get("centers", {})


settings = Settings()  # 全域實例
