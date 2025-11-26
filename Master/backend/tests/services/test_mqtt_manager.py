from pytest import mark

from unittest.mock import AsyncMock, MagicMock, patch

from src.services.mqtt import MQTTManager


class DummyConfig:
    mqtt_broker_host    = 'localhost'
    mqtt_broker_port    = 1883
    topic_device        = 'device'
    topic_configuration = 'config'
    topic_registration  = 'register'
    topic_telemetry     = 'telemetry'
    mqtt_retry_delay    = 0.01


@mark.asyncio
async def test_handle_configuration_publishes():
    manager = MQTTManager(DummyConfig())

    payload = {
        'mode'           : 'auto',
        'sleep_interval' : 10,
    }

    with patch('src.services.mqtt.Client') as MockClient:
        mock_client = AsyncMock()
        MockClient.return_value.__aenter__.return_value = mock_client

        await manager._handle_configuration('dev1', payload)

        mock_client.publish.assert_awaited()


@mark.asyncio
async def test_handle_registration_adds_and_updates():
    device_repo = MagicMock()
    device_repo.get    = AsyncMock(return_value=None)
    device_repo.add    = AsyncMock()
    device_repo.update = AsyncMock()

    manager = MQTTManager(DummyConfig(), device_repo=device_repo)

    with patch('src.services.mqtt.async_session') as mock_session:
        mock_session.return_value.__aenter__.return_value = AsyncMock()
        await manager._handle_registration('dev1')
        device_repo.add.assert_awaited()

        device_repo.get = AsyncMock(return_value=MagicMock())

        await manager._handle_registration('dev1')
        device_repo.update.assert_awaited()


@mark.asyncio
async def test_handle_telemetry_adds():
    telemetry_repo = MagicMock()
    telemetry_repo.add = AsyncMock()

    manager = MQTTManager(DummyConfig(), telemetry_repo=telemetry_repo)

    payload = {
        'sensor_type' : 'temp',
        'value'       : 42,
    }

    with patch('src.services.mqtt.async_session') as mock_session:
        mock_session.return_value.__aenter__.return_value = AsyncMock()
        await manager._handle_telemetry('dev1', payload)

        telemetry_repo.add.assert_awaited()
