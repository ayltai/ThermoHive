from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from ..data.models import Device, OutboxEvent, Relay
from ..data.repositories import DeviceRepository, OutboxRepository, RelayRepository, TelemetryRepository
from ..data import async_session
from ..services import DecisionEngine
from ..utils import log_debug

engine = DecisionEngine()


async def evaluate():
    async with async_session() as session:
        device_repo    = DeviceRepository()
        outbox_repo    = OutboxRepository()
        relay_repo     = RelayRepository()
        telemetry_repo = TelemetryRepository()

        log_debug('Starting evaluation cycle')

        actuator = await device_repo.get_by_actuator(session)
        if not actuator:
            return

        current_state = await relay_repo.get_current_state(session, actuator.id)

        log_debug(f'Current actuator state: {current_state}')

        values: list[float] = []

        # pylint: disable=no-member
        devices = await device_repo.list(session, Device.mode.contains('sensor'))
        for device in devices:
            telemetry = await telemetry_repo.get_latest_for_device(session, device.id, 'temperature')
            if telemetry:
                values.append(telemetry.value)

        decision = await engine.decide(values)
        if decision is None:
            return

        log_debug(f'Decision made: {"ON" if decision else "OFF"}')

        if (decision and current_state == 1) or (not decision and current_state == 0):
            return

        log_debug('Updating actuator state')

        relay = await _upsert_relay(session, relay_repo, actuator.id, 1 if decision else 0)

        await _upsert_event(session, outbox_repo, actuator.id, relay.state)

        await session.commit()


async def _upsert_relay(session: AsyncSession, relay_repo: RelayRepository, actuator_id: str, state: int) -> Relay:
    relay = await relay_repo.get_latest(session, actuator_id)
    if relay:
        await relay_repo.update(session, relay, timestamp=datetime.now(timezone.utc), state=state)
    else:
        relay = Relay()
        relay.device_id = actuator_id
        relay.timestamp = datetime.now(timezone.utc)
        relay.state     = state

        await relay_repo.add(session, relay)

    return relay


async def _upsert_event(session: AsyncSession, outbox_repo: OutboxRepository, actuator_id: str, state: int) -> OutboxEvent:
    await outbox_repo.delete_pending(session, actuator_id, 'relay_state_changed')

    event = OutboxEvent()
    event.device_id  = actuator_id
    event.event_type = 'relay_state_changed'
    event.payload    = {
        'device_id' : actuator_id,
        'state'     : state,
    }

    return await outbox_repo.add(session, event)
