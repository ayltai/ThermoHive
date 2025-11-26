ENVIRONMENT : str = 'esp32'

TOPIC_DEVICE       : str = 'thermohive/control/device'
TOPIC_REGISTRATION : str = 'thermohive/control/registration'
TOPIC_TELEMETRY    : str = 'thermohive/control/telemetry'
TOPIC_RELAY_STATE  : str = 'thermohive/control/relay'

LED_PIN : int = 8

SHT20_PIN_SCL : int = 20
SHT20_PIN_SDA : int = 21

VOLTAGE_PIN : int = 1
RELAY_PIN   : int = 2

VOLTAGE_FULL  : float = 3 * 1.5
VOLTAGE_EMPTY : float = 3 * 1.1

VOLTAGE_DIVIDER_RATIO : float = 5.0
