from abc import ABC, abstractmethod
from typing import Iterable, Optional


class BaseStrategy(ABC):
    @abstractmethod
    async def evaluate(self, values: Iterable[float]) -> Optional[bool]:
        pass
