from typing import Iterable, Optional

from ..strategies import AvgStrategy, MinStrategy
from ..utils.config import AppConfig

STRATEGIES = {
    'avg': AvgStrategy,
    'min': MinStrategy,
}


class DecisionEngine:
    def __init__(self, config: AppConfig = None):
        self.config   = config or AppConfig()
        self.strategy = STRATEGIES.get(getattr(self.config, 'heating_decision_strategy', 'min'), MinStrategy)()

    async def decide(self, values: Iterable[float]) -> Optional[bool]:
        return await self.strategy.evaluate(values)
