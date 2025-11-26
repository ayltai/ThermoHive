from src.sensors.dummy_sensor import DummySensor

def test_dummy_sensor_read():
    sensor = DummySensor()
    data   = sensor.read()

    assert isinstance(data, dict)
    assert data['temperature'] == 25
    assert data['humidity'] == 50
