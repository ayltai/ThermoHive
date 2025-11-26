from asyncio import create_task, gather, Queue, sleep

from datetime import datetime, timezone
from json import dumps, JSONDecodeError, loads

from aiomqtt import Client, MqttError

from ..data.models import Device, Telemetry
from ..data.repositories import DeviceRepository, TelemetryRepository
from ..data import async_session
from ..utils import AppConfig, log_debug, log_error


class MQTTManager:
    def __init__(self, config: AppConfig, device_repo: DeviceRepository = None, telemetry_repo: TelemetryRepository = None) -> None:
        self.queue          : Queue               = Queue()
        self.config         : AppConfig           = config
        self.device_repo    : DeviceRepository    = device_repo or DeviceRepository()
        self.telemetry_repo : TelemetryRepository = telemetry_repo or TelemetryRepository()

    async def _handle_configuration(self, device_id: str, payload: dict) -> None:
        try:
            configuration: dict[str, str | int] = {
                'mode'           : payload['mode'],
                'sleep_interval' : payload['sleep_interval'],
            }

            log_debug(f"Publishing configuration for device {device_id} in mode: {payload['mode']}")

            async with Client(self.config.mqtt_broker_host, self.config.mqtt_broker_port, identifier='processor') as client:
                await client.publish(f"{self.config.topic_device}/{device_id}", dumps(configuration), qos=1, retain=True)
        # pylint: disable=broad-exception-caught
        except Exception as e:
            log_error(e)

    async def _handle_registration(self, device_id: str) -> None:
        try:
            log_debug(f'Registering device {device_id}')

            async with async_session() as session:
                device = await self.device_repo.get(session, Device.id == device_id)
                if device:
                    await self.device_repo.update(session, device, last_seen=datetime.now(timezone.utc))
                else:
                    device = Device()

                    device.id           = device_id
                    device.display_name = None
                    device.mode         = None
                    device.last_seen    = datetime.now(timezone.utc)

                    await self.device_repo.add(session, device)
        # pylint: disable=broad-exception-caught
        except Exception as e:
            log_error(e)

    async def _handle_telemetry(self, device_id: str, payload: dict) -> None:
        try:
            log_debug(f'Receiving telemetry from device {device_id}: type={payload["sensor_type"]}, value={payload["value"]}')

            async with async_session() as session:
                telemetry = Telemetry()

                telemetry.device_id   = device_id
                telemetry.timestamp   = datetime.now(timezone.utc)
                telemetry.sensor_type = payload['sensor_type']
                telemetry.value       = payload['value']

                await self.telemetry_repo.add(session, telemetry)
        # pylint: disable=broad-exception-caught
        except Exception as e:
            log_error(e)

    async def _process_queue(self) -> None:
        while True:
            topic, payload = await self.queue.get()

            topic_parts: list[str] = str(topic).split('/')
            if len(topic_parts) != 4:
                log_error(Exception('Invalid topic format, skipping message'))
                continue

            # pylint: disable=unused-variable
            app_type, domain, message_type, device_id = topic_parts

            try:
                payload = loads(payload.decode())
            except JSONDecodeError as e:
                log_error(e)
                continue

            if message_type == 'configuration':
                await self._handle_configuration(device_id, payload)
            elif message_type == 'registration':
                await self._handle_registration(device_id)
            elif message_type == 'telemetry':
                await self._handle_telemetry(device_id, payload)

            self.queue.task_done()

    async def _mqtt_worker(self) -> None:
        while True:
            try:
                async with Client(self.config.mqtt_broker_host, self.config.mqtt_broker_port, identifier='worker') as client:
                    await client.subscribe(f'{self.config.topic_configuration}/+')
                    await client.subscribe(f'{self.config.topic_registration}/+')
                    await client.subscribe(f'{self.config.topic_telemetry}/+')

                    async for message in client.messages:
                        log_debug(f'Received MQTT message on topic {message.topic}')

                        self.queue.put_nowait((message.topic, message.payload))
            except MqttError as e:
                log_error(e)

                await sleep(self.config.mqtt_retry_delay)

    async def start(self) -> None:
        processor = create_task(self._process_queue())
        worker    = create_task(self._mqtt_worker())

        await gather(processor, worker)
