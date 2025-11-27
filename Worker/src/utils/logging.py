from src.configs import TOPIC_CRASH
from src.services import BaseMQTTManager


def log_debug(message: str) -> None:
    print(f'[DEBUG] {message}')


def log_error(e: Exception) -> None:
    print(f'[ERROR] {type(e).__name__}: {e}')

    raise e

def log_crash(e: Exception, device_id: str, mqtt_manager: BaseMQTTManager) -> None:
    mqtt_manager.publish(f'{TOPIC_CRASH}/{device_id}', f'{type(e).__name__}: {e}', retain=True)
