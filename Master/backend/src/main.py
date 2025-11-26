from asyncio import create_task
from contextlib import asynccontextmanager
from os import path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .data import init_db
from .data.repositories import DeviceRepository, RelayRepository, TelemetryRepository
from .routers import DeviceRouter, RelayRouter, SettingsRouter, TelemetryRouter
from .schedules import consume_outbox, evaluate, start_scheduler
from .services import MQTTManager
from .utils import AppConfig

app_config = AppConfig()


class SpaStaticFiles(StaticFiles):
    # pylint: disable=redefined-outer-name
    def lookup_path(self, path: str):
        full_path, stat_result = super().lookup_path(path)
        if stat_result is None:
            full_path, stat_result = super().lookup_path('index.html')
        return full_path, stat_result


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()

    scheduler = await start_scheduler()
    scheduler.add_job(evaluate, 'interval', minutes=app_config.heating_evaluation_interval, id='evaluation_job', replace_existing=True)
    scheduler.add_job(consume_outbox, 'interval', minutes=app_config.heating_evaluation_interval, id='outbox_consumer_job', replace_existing=True)

    create_task(MQTTManager(app_config).start())

    yield


app = FastAPI(title='ThermoHive Master', version='v1', lifespan=lifespan)

device_repo    = DeviceRepository()
telemetry_repo = TelemetryRepository()
relay_repo     = RelayRepository()

app.include_router(DeviceRouter(app_config, device_repo).router)
app.include_router(RelayRouter(app_config, relay_repo).router)
app.include_router(SettingsRouter().router)
app.include_router(TelemetryRouter(app_config, telemetry_repo).router)

app.add_middleware(CORSMiddleware, expose_headers=['X-Total-Count'], allow_headers=['*'], allow_methods=['*'], allow_origins=['*'])

if app_config.environment != 'dev':
    app.mount('/web', SpaStaticFiles(directory=path.join(path.dirname(__file__), '..', 'web'), html=True), name='web')
