from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from ..utils import AppConfig
from .models import Settings
from .repositories import SettingsRepository

app_config   = AppConfig()
DATABASE_URL = 'sqlite+aiosqlite:////opt/thermohive/database.db' if app_config.environment == 'prod' else 'sqlite+aiosqlite:///database.db'

engine = create_async_engine(DATABASE_URL, future=True)

async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    await init_settings()


async def init_settings():
    async with async_session() as session:
        settings = Settings()
        repo     = SettingsRepository()

        existing = await repo.get(session, Settings.id == 1)
        if not existing:
            settings.id                = 1
            settings.threshold_on      = 17.5
            settings.threshold_off     = 18.5
            settings.decision_strategy = 'min'

            session.add(settings)

            await session.commit()
