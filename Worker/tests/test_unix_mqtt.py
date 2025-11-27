from unittest.mock import MagicMock, patch

from src.networks.dummy_wifi import WiFiManager
from src.services.unix_mqtt import MQTTManager

def test_connect_and_publish():
    with patch('src.services.unix_mqtt.Client') as MockClient:
        mock_client = MagicMock()
        MockClient.return_value = mock_client

        manager = MQTTManager(WiFiManager(), 'dev1', 'localhost', 1883)

        mock_client.is_connected.return_value = False
        mock_client.connect.return_value      = None
        mock_client.loop_start.return_value   = None
        mock_client.subscribe.return_value    = None
        mock_client.publish.return_value      = None

        manager.publish('topic', 'msg')

        mock_client.connect.assert_called_with('localhost', 1883, keepalive=60)
        mock_client.publish.assert_called_with('topic', 'msg', qos=1, retain=False)

        mock_client.is_connected.return_value = True

        manager.publish('topic2', 'msg2')

        mock_client.publish.assert_called_with('topic2', 'msg2', qos=1, retain=False)
