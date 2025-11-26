from datetime import datetime, timedelta, timezone
from typing import Optional, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Device
from .base import AsyncRepository

OFFLINE_THRESHOLD_MINUTES: int = 60


class DeviceRepository(AsyncRepository[Device]):
    def __init__(self):
        super().__init__(Device)

    async def get_by_id(self, session: AsyncSession, id: str) -> Optional[Device]:
        # pylint: disable=unexpected-keyword-arg
        return await self.get(session, Device.id == id)

    async def get_by_actuator(self, session: AsyncSession) -> Optional[Device]:
        # pylint: disable=no-member,unexpected-keyword-arg
        return await self.get(session, Device.mode.contains('actuator'))

    async def list_offline(self, session: AsyncSession, offline_threshold_minutes: int = OFFLINE_THRESHOLD_MINUTES) -> Sequence[Device]:
        # pylint: disable=no-member
        return await self.list(session, Device.last_seen < datetime.now(timezone.utc) - timedelta(minutes=offline_threshold_minutes), order_by=Device.last_seen.asc())
