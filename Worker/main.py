from src import configs, secrets
from src.networks import BaseWiFiManager
from src.services import Worker
from src.utils.logging import log_crash

if configs.ENVIRONMENT == 'unix':
    from sys import exit

    from src.data.unix_storage import Storage
    from src.networks.dummy_bluetooth import BluetoothManager
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
    from webrepl import stop

    # pylint: disable=ungrouped-imports
    from src.data.esp32_storage import Storage
    from src.networks.esp32_bluetooth import BluetoothManager
    from src.networks.esp32_wifi import WiFiManager
    from src.sensors.sht20_sensor import SHT20Sensor
    from src.sensors.voltage_sensor import VoltageSensor
    from src.services.esp32_mqtt import MQTTManager

    Pin(configs.LED_PIN, Pin.OUT).value(0)

    for pin in [0, 3, 4, 5, 6, 7, 9, 10]:
        Pin(pin, Pin.IN, pull=None)

    stop()

    sensors : list[SHT20Sensor] = [
        SHT20Sensor(),
        VoltageSensor(),
    ]

    device_id : bytes = unique_id()

    def sleep(duration: int | None = None) -> None:
        Pin(configs.LED_PIN, Pin.OUT).value(1)

        deepsleep(duration)
else:
    raise RuntimeError(f'Unknown environment in configuration: {configs.ENVIRONMENT}')

# pylint: disable=invalid-name
id           : str             = ''.join(f'{b:02x}' for b in device_id)
wifi_manager : BaseWiFiManager = WiFiManager()
mqtt_manager : MQTTManager     = MQTTManager(wifi_manager, id, secrets.MQTT_BROKER, secrets.MQTT_PORT)

print(f'Starting device with ID: {id}')

try:
    Worker(
        device_id=id,
        sensors=sensors,
        storage=Storage(),
        bluetooth_manager=BluetoothManager(),
        wifi_manager=wifi_manager,
        mqtt_manager=mqtt_manager,
        deepsleep=sleep
    ).run()
except Exception as e:
    log_crash(e, device_id=id, mqtt_manager=mqtt_manager)
