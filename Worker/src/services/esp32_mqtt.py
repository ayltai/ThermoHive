# pylint: disable=import-error
from umqtt.simple import MQTTClient

from src.configs import TOPIC_DEVICE, TOPIC_RELAY_STATE
from src.networks import BaseWiFiManager
from src.services.base_mqtt import BaseMQTTManager
from src.utils import log_error


class MQTTManager(BaseMQTTManager):
    def __init__(self, wifi_manager: BaseWiFiManager, device_id: str, server: str, port: int = 1883) -> None:
        super().__init__(wifi_manager, device_id, server, port)

        self.client = MQTTClient(device_id, server, port, keepalive=60)

    def _ensure_mqtt(self):
        try:
            self.client.ping()

            return True
        # pylint: disable=broad-exception-caught
        except Exception:
            return self._connect_mqtt()

    def _connect_mqtt(self) -> bool:
        if not self.wifi_manager.ensure_wifi_on():
            return False

        try:
            self.client.set_callback(self._mqtt_callback)
            self.client.connect()
            self.client.subscribe(f'{TOPIC_DEVICE}/{self.device_id}', qos=1)
            self.client.subscribe(f'{TOPIC_RELAY_STATE}/{self.device_id}', qos=1)

            return True
        # pylint: disable=broad-exception-caught
        except Exception as e:
            log_error(e)

            return False

    def publish(self, topic: str, msg: str, retain: bool = False) -> None:
        if not self._ensure_mqtt():
            return

        try:
            self.client.publish(topic, msg, qos=1, retain=retain)
        # pylint: disable=broad-exception-caught
        except Exception as e:
            log_error(e)
