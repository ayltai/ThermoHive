from src.networks.base_wifi import BaseWiFiManager


class WiFiManager(BaseWiFiManager):
    def ensure_wifi(self) -> bool:
        return True
