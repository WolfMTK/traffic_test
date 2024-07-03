from contextlib import asynccontextmanager, AbstractAsyncContextManager
from typing import AsyncIterator

from fastapi import Depends

from app.application.commands.create_traffic_large import CreateTrafficLarge
from app.application.commands.create_traffic_small import CreateTrafficSmall
from app.application.commands.get_traffic_large import GetTrafficLarge
from app.application.commands.get_traffic_small import GetTrafficSmall
from app.application.commands.get_traffics_large import GetTrafficsLarge
from app.application.commands.get_traffics_small import GetTrafficsSmall
from app.application.commands.update_traffic_large import UpdateTrafficLarge
from app.application.commands.update_traffic_small import UpdateTrafficSmall
from app.application.protocols.repository_traffic_large import ALargeTrafficRepository
from app.application.protocols.repository_traffic_small import ASmallTrafficRepository
from app.domain.service.traffic_large import TrafficLargeService
from app.domain.service.traffic_small import TrafficSmallService
from app.presentation.traffic_large_interactor import TrafficLargeInteractorFactory
from app.presentation.traffic_small_interactor import TrafficSmallInteractorFactory


class TrafficLargeIOC(TrafficLargeInteractorFactory):
    def __init__(self,
                 repository: ALargeTrafficRepository = Depends(ALargeTrafficRepository)) -> None:
        self.repository = repository
        self.service = TrafficLargeService()

    @asynccontextmanager
    async def create_traffic(self) -> AsyncIterator[CreateTrafficLarge]:
        yield CreateTrafficLarge(
            self.repository,
            self.service
        )

    @asynccontextmanager
    async def update_traffic(self) -> AsyncIterator[UpdateTrafficLarge]:
        yield UpdateTrafficLarge(
            self.repository,
            self.service
        )

    @asynccontextmanager
    async def get_traffics(self) -> AsyncIterator[GetTrafficsLarge]:
        yield GetTrafficsLarge(
            self.repository,
            self.service
        )

    @asynccontextmanager
    async def get_traffic(self) -> AsyncIterator[GetTrafficLarge]:
        yield GetTrafficLarge(
            self.repository,
            self.service
        )


class TrafficSmallIOC(TrafficSmallInteractorFactory):
    def __init__(
            self,
            repository: ASmallTrafficRepository = Depends(ASmallTrafficRepository)
    ) -> None:
        self.repository = repository
        self.service = TrafficSmallService()

    @asynccontextmanager
    async def create_traffic(self) -> AsyncIterator[CreateTrafficSmall]:
        yield CreateTrafficSmall(
            self.repository,
            self.service
        )

    @asynccontextmanager
    async def get_traffic(self) -> AsyncIterator[GetTrafficSmall]:
        yield GetTrafficSmall(
            self.repository,
            self.service
        )

    @asynccontextmanager
    async def get_traffics(self) -> AsyncIterator[GetTrafficsSmall]:
        yield GetTrafficsSmall(
            self.repository,
            self.service
        )

    @asynccontextmanager
    async def update_traffic(self) -> AsyncIterator[UpdateTrafficSmall]:
        yield UpdateTrafficSmall(
            self.repository,
            self.service
        )
