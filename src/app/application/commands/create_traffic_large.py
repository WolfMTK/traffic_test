from app.application.dto.traffic_large import (
    TrafficLargeCreateDTO,
    TrafficLargeResultDTO,
)
from app.application.protocols.interactor import Interactor
from app.application.protocols.repository_traffic_large import (
    ALargeTrafficRepository,
)
from app.domain.service.traffic_large import TrafficLargeService


class CreateTrafficLarge(
    Interactor[TrafficLargeCreateDTO, TrafficLargeResultDTO]
):
    def __init__(self,
                 repository: ALargeTrafficRepository,
                 service: TrafficLargeService):
        self.repository = repository
        self.service = service

    async def __call__(self,
                       data: TrafficLargeCreateDTO) -> TrafficLargeResultDTO:
        traffic = self.service.create_traffic(data.status, data.autos)
        traffic = self.repository.add(traffic)
        return TrafficLargeResultDTO(
            id=traffic.id,
            status=traffic.status,  # type: ignore
            autos=traffic.autos,
            traffics_small=traffic.traffics_small
        )
