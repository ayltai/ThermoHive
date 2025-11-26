from typing import cast

from fastapi import Depends, HTTPException, Path, status

from ..data.models import Relay
from ..data.repositories import RelayRepository
from ..utils.config import AppConfig
from .base import BaseRouter


class RelayRouter(BaseRouter):
    def __init__(self, config: AppConfig, repo: RelayRepository = None) -> None:
        self.config : AppConfig       = config
        self.repo   : RelayRepository = repo or RelayRepository()

        super().__init__(Relay, self.repo, '/api/v1/relays', ['relay'])

    def _setup_routes(self) -> None:
        super()._setup_routes()

        @self.router.get('/current/{device_id}', response_model=int)
        async def get_current_state(device_id: str = Path(...), session=Depends(BaseRouter._get_session)) -> int:
            result = await cast(RelayRepository, self.repo).get_current_state(session, device_id)
            if result is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

            return result
