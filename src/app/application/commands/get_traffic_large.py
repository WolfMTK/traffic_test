import uuid

from app.application.dto.traffic_large import TrafficLargeResultDTO
from app.application.protocols.interactor import Interactor
from app.application.protocols.repository_traffic_large import (
    ALargeTrafficRepository,
)
from app.domain.service.traffic_large import TrafficLargeService


class GetTrafficLarge(Interactor[uuid.UUID, TrafficLargeResultDTO]):
    def __init__(self,
                 repository: ALargeTrafficRepository,
                 service: TrafficLargeService):
        self.repository = repository
        self.service = service

    async def __call__(self, data: uuid.UUID) -> TrafficLargeResultDTO:
        traffic = self.repository.get(data)
        traffic = self.service.get_traffic(traffic)
        return TrafficLargeResultDTO(
            id=traffic.id,
            status=traffic.status,  # type: ignore
            autos=traffic.autos,
            traffics_small=traffic.traffics_small
        )
