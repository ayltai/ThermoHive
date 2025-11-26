from pytest import fixture

from unittest.mock import MagicMock

from src.data import BaseStorage
from src.networks.dummy_wifi import WiFiManager
from src.sensors import BaseSensor
from src.services import BaseMQTTManager
from src.services.worker import Worker

wifi_manager = WiFiManager()


class DummySensor(BaseSensor):
    def read(self):
        return {
            'temperature' : 22,
            'humidity'    : 55,
        }


class DummyStorage(BaseStorage):
    def __init__(self):
        self.values = {}

    def get_int(self, key):
        return self.values.get(key)

    def set_int(self, key, value):
        self.values[key] = value


class DummyMQTT(BaseMQTTManager):
    def __init__(self, device_id: str, server: str):
        super().__init__(wifi_manager, device_id, server)

        self.published = []
        self.callback  = None

    def set_on_callback(self, cb):
        self.callback = cb

    def publish(self, topic, msg):
        self.published.append((topic, msg))


@fixture
def worker():
    return Worker(
        device_id='dev1',
        sensors=[DummySensor()],
        storage=DummyStorage(),
        wifi_manager=wifi_manager,
        mqtt_manager=DummyMQTT('dev1', 'mqtt://test'),
        deepsleep=MagicMock()
    )

def test_register_publishes(worker: Worker):
    worker.register()

    assert any('registration' in topic for topic, _ in worker.mqtt_manager.published)

def test_publish_telemetry(worker):
    worker.mode = 'sensor'

    worker.publish()

    assert any('telemetry' in topic for topic, _ in worker.mqtt_manager.published)

def test_on_mqtt_message_config(worker: Worker):
    payload = {
        'mode'           : 'sensor',
        'sleep_interval' : 10,
    }

    worker._on_mqtt_message('thermohive/control/device/dev1', payload)

    assert worker.mode           == 'sensor'
    assert worker.sleep_interval == 10

def test_on_mqtt_message_relay(worker: Worker):
    worker.mode         = 'actuator'
    worker.toggle_relay = MagicMock()

    payload = {
        'state' : 1,
    }

    worker._on_mqtt_message('thermohive/control/relay/dev1', payload)

    assert worker.relay_toggle_requested
    assert worker.target_relay_state == 1

    worker.toggle_relay.assert_called_once()

def test_toggle_relay_sets_state(worker: Worker):
    worker.mode               = 'actuator'
    worker.target_relay_state = 1

    worker.storage.set_int('relay_state', 0)

    worker.toggle_relay()

    assert worker.storage.get_int('relay_state') == 1
    assert worker.relay_toggle_requested is False
    assert worker.target_relay_state is None

def test_run_sensor(monkeypatch, worker: Worker):
    worker.mode           = 'sensor'
    worker.sleep_interval = 1
    worker.publish        = MagicMock()

    monkeypatch.setattr('time.time', lambda: 0)
    monkeypatch.setattr('time.sleep', lambda x: None)

    worker.run()

    worker.publish.assert_called_once()
    worker.deepsleep.assert_called()

def test_run_actuator(monkeypatch, worker: Worker):
    worker.mode                   = 'actuator'
    worker.sleep_interval         = 1
    worker.relay_toggle_requested = True
    worker.toggle_relay           = MagicMock()

    monkeypatch.setattr('time.time', lambda: 0)
    monkeypatch.setattr('time.sleep', lambda x: None)

    worker.run()

    worker.toggle_relay.assert_called_once()
    worker.deepsleep.assert_called()
