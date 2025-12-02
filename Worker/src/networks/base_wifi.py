from src.utils.base import BaseWatchdog


class BaseWiFiManager:
    def __init__(self, watchdog: BaseWatchdog):
        self.watchdog = watchdog

    def ensure_wifi_on(self) -> bool:
        pass

    def ensure_wifi_off(self) -> bool:
        pass
