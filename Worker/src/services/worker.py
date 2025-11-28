from json import dumps
from time import sleep, time

from src.data import BaseStorage
from src.networks import BaseBluetoothManager, BaseWiFiManager
from src.sensors import BaseSensor
from src.services.base_mqtt import BaseMQTTManager
from src.utils.base import BaseWatchdog
from src.utils.logging import log_debug
from src import configs

MODES = [
    'actuator',
    'sensor',
]

DEADLINE = 120


class Worker:
    def __init__(
        self,
        device_id         : str,
        sensors           : list[BaseSensor],
        storage           : BaseStorage,
        bluetooth_manager : BaseBluetoothManager,
        wifi_manager      : BaseWiFiManager,
        mqtt_manager      : BaseMQTTManager,
        watchdog          : BaseWatchdog,
        deepsleep
    ) -> None:
        self.device_id              = device_id
        self.sensors                = sensors
        self.storage                = storage
        self.wifi_manager           = wifi_manager
        self.mqtt_manager           = mqtt_manager
        self.watchdog               = watchdog
        self.deepsleep              = deepsleep

        self.mode                   : str | None = None
        self.sleep_interval         : int        = 300
        self.relay_toggle_requested : bool       = False
        self.target_relay_state     : int | None = None

        self.mqtt_manager.set_on_callback(self._on_mqtt_message)

        bluetooth_manager.ensure_bluetooth_disabled()

    def _on_mqtt_message(self, topic: str, payload: dict) -> None:
        log_debug(f'Received MQTT message on topic {topic}:\n{dumps(payload)}')

        if topic == f'{configs.TOPIC_DEVICE}/{self.device_id}':
            self.mode           = payload.get('mode', self.mode)
            self.sleep_interval = payload.get('sleep_interval', self.sleep_interval)
        elif topic == f'{configs.TOPIC_RELAY_STATE}/{self.device_id}':
            self.relay_toggle_requested = 'state' in payload
            if self.relay_toggle_requested:
                self.target_relay_state = payload['state']

            if 'actuator' in self.mode:
                self.toggle_relay()

    def register(self) -> None:
        log_debug(f'Registering device {self.device_id}...')

        self.mqtt_manager.publish(f'{configs.TOPIC_REGISTRATION}/{self.device_id}', dumps({
            'device_id': self.device_id,
        }))

    def publish(self) -> None:
        for sensor in self.sensors:
            try:
                readings = sensor.read()

                for sensor_type, value in readings.items():
                    data = {
                        'device_id'   : self.device_id,
                        'sensor_type' : sensor_type,
                        'value'       : value,
                    }

                    log_debug(f'Publishing telemetry data for device {self.device_id}:\n{dumps(data)}')

                    self.mqtt_manager.publish(f'{configs.TOPIC_TELEMETRY}/{self.device_id}', dumps(data))
            # pylint: disable=broad-exception-caught
            except Exception as e:
                log_debug(f'Error reading from sensor {sensor.__class__.__name__}: {e}')
                continue

    def toggle_relay(self) -> None:
        current_state = self.storage.get_int('relay_state')
        log_debug(f'Current relay state: {current_state}, Target relay state: {self.target_relay_state}')

        if current_state is None or current_state != self.target_relay_state:
            log_debug('Toggling relay...')
            if configs.ENVIRONMENT == 'esp32':
                # pylint: disable=import-error, import-outside-toplevel
                from machine import Pin

                relay_pin = Pin(configs.RELAY_PIN, Pin.OUT)
                relay_pin.value(1)
                sleep(0.5)
                relay_pin.value(0)

            self.storage.set_int('relay_state', self.target_relay_state)

            self.relay_toggle_requested = False
            self.target_relay_state     = None

    def run(self) -> None:
        self.register()

        self.watchdog.feed()

        deadline = time() + DEADLINE
        while time() < deadline:
            if self.mode:
                break

            self.watchdog.feed()

            sleep(1)

        if not self.mode:
            log_debug('No configuration received, entering deepsleep...')

            self.deepsleep(self.sleep_interval * 1000)

        if 'sensor' in self.mode:
            self.publish()
        elif 'actuator' in self.mode:
            if self.relay_toggle_requested:
                self.toggle_relay()

        self.watchdog.feed()

        self.wifi_manager.ensure_wifi_off()

        log_debug(f'Deepsleeping for {self.sleep_interval} seconds...')
        self.deepsleep(self.sleep_interval * 1000)
