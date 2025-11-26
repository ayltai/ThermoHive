from paho.mqtt.client import Client

from src.configs import TOPIC_DEVICE, TOPIC_RELAY_STATE
from src.networks import BaseWiFiManager
from src.services.base_mqtt import BaseMQTTManager
from src.utils import log_debug


class MQTTManager(BaseMQTTManager):
    def __init__(self, wifi_manager: BaseWiFiManager, device_id: str, server: str, port: int = 1883) -> None:
        super().__init__(wifi_manager, device_id, server, port)

        self.client = Client(client_id=device_id, clean_session=False, reconnect_on_failure=True)

    # pylint: disable=unused-argument
    def _on_message(self, client, userdata, message):
        log_debug(f'MQTT Message Received: Topic={message.topic}, Payload={message.payload}')
        self._mqtt_callback(message.topic.encode(), message.payload)

    def _ensure_mqtt(self):
        if self.client.is_connected():
            log_debug('MQTT already connected')
            return True

        return self._connect_mqtt()

    def _connect_mqtt(self) -> bool:
        log_debug('Connecting to MQTT broker...')

        self.client.connect(self.server, self.port, keepalive=60)

        self.client.on_message = self._on_message

        self.client.subscribe(f'{TOPIC_DEVICE}/{self.device_id}', qos=1)
        self.client.subscribe(f'{TOPIC_RELAY_STATE}/{self.device_id}', qos=1)

        self.client.loop_start()

        return True

    def publish(self, topic: str, msg: str):
        if not self._ensure_mqtt():
            return

        self.client.publish(topic, msg, qos=1)
