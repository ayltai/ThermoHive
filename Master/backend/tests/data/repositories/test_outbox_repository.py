from pytest import mark

from unittest.mock import AsyncMock

from src.data.models import OutboxEvent
from src.data.repositories import OutboxRepository


@mark.asyncio
async def test_get_next():
    repo    = OutboxRepository()
    session = AsyncMock()
    event   = OutboxEvent(device_id='dev1', event_type='type', is_processed=False)

    repo.list = AsyncMock(return_value=[event])

    result = await repo.get_next(session, 'dev1', 'type')

    assert result == event


@mark.asyncio
async def test_delete_pending():
    repo    = OutboxRepository()
    session = AsyncMock()
    event   = OutboxEvent(device_id='dev1', event_type='type', is_processed=False)

    repo.list = AsyncMock(return_value=[event])
    repo.delete = AsyncMock()

    await repo.delete_pending(session, 'dev1', 'type')

    repo.delete.assert_awaited_with(session, event)
