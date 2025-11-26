from pytest import mark

from sqlmodel import SQLModel, Field
from unittest.mock import AsyncMock, MagicMock

from src.data.repositories import AsyncRepository


class DummyModel(SQLModel, table=True):
    id : int = Field(primary_key=True)


@mark.asyncio
async def test_add_and_get():
    repo    = AsyncRepository(DummyModel)
    session = AsyncMock()
    dummy   = DummyModel(id=1)

    session.add     = MagicMock()
    session.commit  = AsyncMock()
    session.refresh = AsyncMock()

    await repo.add(session, dummy)

    session.add.assert_called_once_with(dummy)
    session.commit.assert_awaited()
    session.refresh.assert_awaited_with(dummy)
