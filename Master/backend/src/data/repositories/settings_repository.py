from ..models import Settings
from .base import AsyncRepository


class SettingsRepository(AsyncRepository[Settings]):
    def __init__(self):
        super().__init__(Settings)
