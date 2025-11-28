from src.networks.dummy_wifi import WiFiManager
from src.utils.dummy_watchdog import Watchdog

def test_dummy_wifi_connect():
    wifi = WiFiManager(Watchdog())

    assert hasattr(wifi, 'ensure_wifi_on')
    assert callable(wifi.ensure_wifi_on)

    assert hasattr(wifi, 'ensure_wifi_off')
    assert callable(wifi.ensure_wifi_off)
