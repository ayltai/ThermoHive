# pylint: disable=import-error
from machine import WDT

from src.utils.base import BaseWatchdog

WATCHDOG_TIMEOUT_MS : int = 15000

# pylint: disable=invalid-name
watchdog : WDT | None = None


class Watchdog(BaseWatchdog):
    def __init__(self) -> None:
        global watchdog
        if watchdog is None:
            watchdog = WDT(timeout=WATCHDOG_TIMEOUT_MS)

    def feed(self) -> None:
        global watchdog
        if watchdog is not None:
            watchdog.feed()
