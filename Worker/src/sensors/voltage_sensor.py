# pylint: disable=import-error
from machine import ADC, Pin

from src.sensors.base import BaseSensor
from src.utils.logging import log_debug
from src import configs


class VoltageSensor(BaseSensor):
    def __init__(self, pin: int = configs.VOLTAGE_PIN, voltage_full: float = configs.VOLTAGE_FULL, voltage_empty: float = configs.VOLTAGE_EMPTY, ratio: float = configs.VOLTAGE_DIVIDER_RATIO):
        self.pin = ADC(Pin(pin))

        self.voltage_full  = voltage_full
        self.voltage_empty = voltage_empty
        self.ratio         = ratio

    def read(self) -> dict:
        return {
            'battery' : max(0.0, min(100.0, ((self.read_raw() - self.voltage_empty) / (self.voltage_full - self.voltage_empty)) * 100.0)),
        }

    def read_raw(self) -> float:
        value = (self.pin.read_u16() / 65535.0) * 3.3 * self.ratio
        log_debug(f'Voltage reading: {value:.2f} V')

        return value
