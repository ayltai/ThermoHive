# pylint: disable=import-error
from network import STA_IF, WLAN
# pylint: disable=wrong-import-order
from time import sleep

from src.secrets import WIFI_PASSWORD, WIFI_SSID
from src.networks.base_wifi import BaseWiFiManager
from src.utils.logging import log_debug

TIMEOUT: int = 30


class WiFiManager(BaseWiFiManager):
    def __init__(self):
        self.wlan = WLAN(STA_IF)

    def ensure_wifi_on(self) -> bool:
        self.wlan.active(True)

        if not self.wlan.isconnected():
            log_debug(f'Connecting to WiFi SSID: {WIFI_SSID}')
            self.wlan.connect(WIFI_SSID, WIFI_PASSWORD)

            timeout: int = 0
            while not self.wlan.isconnected() and timeout < TIMEOUT:
                sleep(1)

                timeout += 1

        log_debug(f'WiFi connected: {self.wlan.ifconfig()}')
        return self.wlan.isconnected()

    def ensure_wifi_off(self) -> bool:
        self.wlan.active(False)
        log_debug('WiFi turned off')

        return not self.wlan.isconnected()
