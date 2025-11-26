from src.sensors.base import BaseSensor


class DummySensor(BaseSensor):
    def read(self) -> dict:
        return {
            'temperature' : 25,
            'humidity'    : 50,
        }
