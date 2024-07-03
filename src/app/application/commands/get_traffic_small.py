import uuid

from app.application.dto.traffic_small import TrafficSmallResultDTO
from app.application.protocols.interactor import Interactor
from app.application.protocols.repository_traffic_small import (
    ASmallTrafficRepository,
)
from app.domain.service.traffic_small import TrafficSmallService


class GetTrafficSmall(Interactor[uuid.UUID, TrafficSmallResultDTO]):
    def __init__(self,
                 repository: ASmallTrafficRepository,
                 service: TrafficSmallService) -> None:
        self.repository = repository
        self.service = service

    async def __call__(self, data: uuid.UUID) -> TrafficSmallResultDTO:
        traffic = self.repository.get(data)
        traffic = self.service.get_traffic(traffic)
        return TrafficSmallResultDTO(
            id=traffic.id,
            status=traffic.status,  # type: ignore
            pedestrians=traffic.pedestrians
        )
