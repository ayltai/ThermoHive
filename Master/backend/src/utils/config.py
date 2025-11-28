from os import path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE : str = '/opt/thermohive/.env'


class AppConfig(BaseSettings):
    environment                 : str = 'dev'
    mqtt_broker_host            : str
    mqtt_broker_port            : int = 1883
    mqtt_retry_delay            : int = 5
    topic_device                : str
    topic_configuration         : str
    topic_registration          : str
    topic_relay_state           : str
    topic_telemetry             : str
    topic_crash_report          : str
    device_sleep_interval       : int = 600
    heating_evaluation_interval : int = 10
    heating_evaluation_strategy : str = 'min'
    outbox_processing_interval  : int = 10

    model_config = SettingsConfigDict(
        env_file=ENV_FILE if path.exists(ENV_FILE) else '.env',
        env_file_encoding='utf-8',
    )
