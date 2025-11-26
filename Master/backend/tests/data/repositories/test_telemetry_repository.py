from pytest import mark

from unittest.mock import AsyncMock

from src.data.models import Telemetry
from src.data.repositories import TelemetryRepository


@mark.asyncio
async def test_get_latest_for_device():
    repo      = TelemetryRepository()
    session   = AsyncMock()
    telemetry = Telemetry(device_id='dev1', sensor_type='temp')

    repo.list = AsyncMock(return_value=[telemetry])

    result = await repo.get_latest_for_device(session, 'dev1', 'temp')

    assert result == telemetry
