from pydantic_settings import BaseSettings, SettingsConfigDict


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
    device_sleep_interval       : int = 600
    heating_evaluation_interval : int = 10
    outbox_processing_interval  : int = 10

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )
