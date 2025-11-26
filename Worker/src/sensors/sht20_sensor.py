# pylint: disable=import-error
from machine import I2C, Pin

from src.libraries import SHT20
from src.sensors.base import BaseSensor
from src import configs


class SHT20Sensor(BaseSensor):
    def __init__(self, scl_pin: int = configs.SHT20_PIN_SCL, sda_pin: int = configs.SHT20_PIN_SDA):
        self.sensor = SHT20(I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin)))

    def read(self) -> dict:
        results = {}

        try:
            results['temperature'] = self.sensor.temperature
        except OSError:
            pass

        try:
            results['humidity'] = self.sensor.humidity
        except OSError:
            pass

        return results
