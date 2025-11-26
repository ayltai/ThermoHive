from src.networks.dummy_wifi import WiFiManager

def test_dummy_wifi_connect():
    wifi = WiFiManager()

    assert hasattr(wifi, 'ensure_wifi')
    assert callable(wifi.ensure_wifi)
