import uuid
from dataclasses import dataclass
from typing import Literal

from app.application.dto.traffic_small import TrafficSmallResultDTO
from app.application.protocols.interactor import Interactor
from app.application.protocols.repository_traffic_small import (
    ASmallTrafficRepository,
)
from app.domain.service.traffic_small import TrafficSmallService


@dataclass
class TrafficSmallCreateDTO:
    id: uuid.UUID
    status: Literal["GREEN", "RED"]
    pedestrians: int


class CreateTrafficSmall(
    Interactor[TrafficSmallCreateDTO, TrafficSmallResultDTO]
):
    def __init__(self,
                 repository: ASmallTrafficRepository,
                 service: TrafficSmallService) -> None:
        self.repository = repository
        self.service = service

    async def __call__(self,
                       data: TrafficSmallCreateDTO) -> TrafficSmallResultDTO:
        traffic = self.service.create_traffic(
            data.status, data.pedestrians, data.id
        )
        traffic = self.repository.add(traffic)
        return TrafficSmallResultDTO(
            id=traffic.id,
            status=traffic.status,  # type: ignore
            pedestrians=traffic.pedestrians,
        )
