from datetime import timezone

from pytest import fixture

from fastapi.testclient import TestClient

from src.main import app


@fixture
def client():
    return TestClient(app)


@fixture
def async_monkeypatch(monkeypatch):
    def _patch(target, value):
        async def wrapper(*args, **kwargs):
            return value(*args, **kwargs) if callable(value) else value

        monkeypatch.setattr(target, wrapper)

    return _patch


def test_device_crud(client, monkeypatch):
    async def async_add(self, session, entity):
        return entity

    async def async_get(self, session, *args, **kwargs):
        return None

    monkeypatch.setattr('src.routers.device.DeviceRepository.add', async_add)
    monkeypatch.setattr('src.routers.device.DeviceRepository.get', async_get)

    response = client.post('/api/v1/devices/', json={
        'id'   : 'dev1',
        'mode' : 'auto',
    })

    assert response.status_code == 201
    assert response.json()['id'] == 'dev1'


def test_relay_current_state(client, monkeypatch):
    async def async_get_current_state(self, session, device_id):
        return 1

    monkeypatch.setattr('src.routers.relay.RelayRepository.get_current_state', async_get_current_state)

    response = client.get('/api/v1/relays/current/dev1')

    assert response.status_code == 200
    assert response.json() == 1


def test_settings_get_by_id(client, monkeypatch):
    async def async_get(self, session, *args, **kwargs):
        return {
            'id' : 1,
        }

    monkeypatch.setattr('src.routers.settings.SettingsRepository.get', async_get)

    response = client.get('/api/v1/settings/1')

    assert response.status_code == 200
    assert response.json()['id'] == 1


def test_telemetry_recent(client, monkeypatch):
    async def async_list(self, session, *args, **kwargs):
        return [type('Device', (), {
            'id'   : 'dev1',
            'mode' : 'sensor',
        })()]

    async def async_get_latest_for_device(self, session, device_id, sensor_type):
        return type('Telemetry', (), {
            'id'          : 1,
            'timestamp'   : __import__('datetime').datetime.now(timezone.utc),
            'device_id'   : device_id,
            'sensor_type' : sensor_type,
            'value'       : 23.5,
        })()

    monkeypatch.setattr('src.routers.telemetry.DeviceRepository.list', async_list)
    monkeypatch.setattr('src.routers.telemetry.TelemetryRepository.get_latest_for_device', async_get_latest_for_device)

    response = client.get('/api/v1/telemetry/recent?offset=1')

    assert response.status_code == 200
    assert isinstance(response.json(), list)
