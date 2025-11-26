from json import dumps

from aiomqtt import Client

from ..data import async_session
from ..data.repositories import DeviceRepository, OutboxRepository
from ..utils.config import AppConfig

app_config = AppConfig()


async def consume_outbox():
    device_repo = DeviceRepository()
    outbox_repo = OutboxRepository()

    async with async_session() as session:
        actuator = await device_repo.get_by_actuator(session)
        if not actuator:
            return

        event = await outbox_repo.get_next(session, actuator.id, 'relay_state_changed')
        if not event:
            return

        await outbox_repo.delete_pending(session, actuator.id, 'relay_state_changed')

        async with Client(app_config.mqtt_broker_host, app_config.mqtt_broker_port) as client:
            await client.publish(f'{app_config.topic_relay_state}/{actuator.id}', dumps(event.payload), qos=1, retain=True)

        await session.commit()
