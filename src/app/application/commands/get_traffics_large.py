from app.application.dto.query import StatusQuery
from app.application.dto.traffic_large import TrafficLargeResultDTO
from app.application.protocols.interactor import Interactor
from app.application.protocols.repository_traffic_large import (
    ALargeTrafficRepository
)
from app.domain.service.traffic_large import TrafficLargeService


class GetTrafficsLarge(Interactor[StatusQuery, list[TrafficLargeResultDTO]]):
    def __init__(self,
                 repository: ALargeTrafficRepository,
                 service: TrafficLargeService):
        self.repository = repository
        self.service = service

    async def __call__(
            self, data: StatusQuery
    ) -> list[TrafficLargeResultDTO]:
        traffics = self.repository.get_all()
        traffics = self.service.sort_status(data.status, traffics)
        return [TrafficLargeResultDTO(
            id=value.id,
            status=value.status,  # type: ignore
            autos=value.autos,
            traffics_small=value.traffics_small
        ) for value in traffics]
