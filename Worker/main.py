from src import configs, secrets
from src.networks import BaseWiFiManager
from src.services import Worker

if configs.ENVIRONMENT == 'unix':
    from sys import exit

    from src.data.unix_storage import Storage
    from src.networks.dummy_wifi import WiFiManager
    from src.sensors.dummy_sensor import DummySensor
    from src.services.unix_mqtt import MQTTManager

    sensors   : list[DummySensor] = [DummySensor()]
    device_id : bytes             = b'TEST_DEVICE_1234'

    def sleep(_: int | None) -> None:
        exit(0)
elif configs.ENVIRONMENT == 'esp32':
    # pylint: disable=import-error
    from machine import deepsleep, Pin, unique_id

    # pylint: disable=ungrouped-imports
    from src.data.esp32_storage import Storage
    from src.networks.esp32_wifi import WiFiManager
    from src.sensors.sht20_sensor import SHT20Sensor
    from src.sensors.voltage_sensor import VoltageSensor
    from src.services.esp32_mqtt import MQTTManager

    Pin(configs.LED_PIN, Pin.OUT).on()

    sensors : list[SHT20Sensor] = [
        SHT20Sensor(),
        VoltageSensor(),
    ]

    device_id : bytes = unique_id()

    def sleep(duration: int | None = None) -> None:
        Pin(configs.LED_PIN, Pin.OUT).off()

        deepsleep(duration)
else:
    raise RuntimeError(f'Unknown environment in configuration: {configs.ENVIRONMENT}')

# pylint: disable=invalid-name
id           : str             = ''.join(f'{b:02x}' for b in device_id)
wifi_manager : BaseWiFiManager = WiFiManager()

print(f'Starting device with ID: {id}')

Worker(
    device_id=id,
    sensors=sensors,
    storage=Storage(),
    wifi_manager=wifi_manager,
    mqtt_manager=MQTTManager(wifi_manager, id, secrets.MQTT_BROKER, secrets.MQTT_PORT),
    deepsleep=sleep
).run()
