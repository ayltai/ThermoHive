from json import dumps
from aiomqtt import Client
from sqlalchemy.ext.asyncio import AsyncSession

from ..data.models import Device
from ..data.repositories import DeviceRepository
from .base import BaseRouter
from ..utils.config import AppConfig


class DeviceRouter(BaseRouter):
    def __init__(self, config: AppConfig, repo: DeviceRepository = None) -> None:
        self.config : AppConfig        = config
        self.repo   : DeviceRepository = repo or DeviceRepository()

        super().__init__(Device, self.repo, '/api/v1/devices', ['device'])

    async def _publish_update(self, entity: Device) -> None:
        configuration = {
            'mode'           : entity.mode,
            'sleep_interval' : self.config.device_sleep_interval,
        }

        async with Client(self.config.mqtt_broker_host, self.config.mqtt_broker_port) as client:
            await client.publish(f'{self.config.topic_configuration}/{entity.id}', dumps(configuration), qos=1, retain=True)

    async def _after_update(self, entity: Device, session: AsyncSession) -> None:
        await super()._after_update(entity, session)

        await self._publish_update(entity)
