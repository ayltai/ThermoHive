from json import dumps

from aiomqtt import Client
from fastapi import Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from ..data.models import Device
from ..data.repositories import DeviceRepository, TelemetryRepository
from ..utils import AppConfig
from .base import BaseRouter


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

    def _setup_routes(self) -> None:
        @self.router.get('/all')
        async def list_all(response: Response, session: AsyncSession = Depends(BaseRouter._get_session), offset: int = Query(None, ge=0), limit: int = Query(None, ge=1, le=100)):
            response.headers['X-Total-Count'] = str(await self.repo.count(session))

            devices                = await self.repo.list(session, offset=offset, limit=limit)
            devices_with_telemetry = []
            telemetry_repo         = TelemetryRepository()

            for device in devices:
                temperature = await telemetry_repo.get_latest_for_device(session, device.id, 'temperature')
                humidity    = await telemetry_repo.get_latest_for_device(session, device.id, 'humidity')
                battery     = await telemetry_repo.get_latest_for_device(session, device.id, 'battery')

                devices_with_telemetry.append({
                    'id'           : device.id,
                    'display_name' : device.display_name,
                    'mode'         : device.mode,
                    'last_seen'    : device.last_seen,
                    'temperature'  : temperature.value if temperature else None,
                    'humidity'     : humidity.value if humidity else None,
                    'battery'      : battery.value if battery else None,
                })

            return devices_with_telemetry

        super()._setup_routes()
