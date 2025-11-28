from json import loads

from src.networks.base_wifi import BaseWiFiManager
from src.utils.base import BaseWatchdog


class BaseMQTTManager:
    def __init__(self, wifi_manager: BaseWiFiManager, watchdog: BaseWatchdog, device_id: str, server: str, port: int = 1883):
        self.server       = server
        self.port         = port
        self.wifi_manager = wifi_manager
        self.watchdog     = watchdog
        self.device_id    = device_id
        self.on_callback  = None

    def set_on_callback(self, on_callback):
        self.on_callback = on_callback

    def _mqtt_callback(self, topic: bytes, msg: bytes):
        if self.on_callback:
            self.on_callback(topic.decode(), loads(msg.decode()))

    def _ensure_mqtt(self):
        pass

    def _connect_mqtt(self) -> bool:
        pass

    # pylint: disable=unused-argument
    def publish(self, topic: str, msg: str, retain: bool = False) -> None:
        pass
