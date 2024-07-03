import uuid
from dataclasses import dataclass, field
from typing import Literal

from app.application.dto.traffic_small import TrafficSmallResultDTO
from app.application.protocols.interactor import Interactor
from app.application.protocols.repository_traffic_small import (
    ASmallTrafficRepository,
)
from app.domain.service.traffic_small import TrafficSmallService


@dataclass
class TrafficSmallUpdateDTO:
    id: uuid.UUID
    status: Literal["GREEN", "RED"] | None = field(default=None)
    pedestrians: int | None = field(default=None)


class UpdateTrafficSmall(
    Interactor[TrafficSmallUpdateDTO, TrafficSmallResultDTO]
):
    def __init__(self,
                 repository: ASmallTrafficRepository,
                 service: TrafficSmallService) -> None:
        self.repository = repository
        self.service = service

    async def __call__(
            self, data: TrafficSmallUpdateDTO
    ) -> TrafficSmallResultDTO:
        traffic = self.repository.get(data.id)
        traffic = self.service.get_traffic(traffic)
        traffic = self.service.update_traffic(
            id=data.id,
            status=data.status,
            pedestrians=data.pedestrians,
            large_traffic_id=traffic.large_traffic_id
        )
        traffic = self.repository.update(traffic)
        return TrafficSmallResultDTO(
            id=traffic.id,
            status=traffic.status,  # type: ignore
            pedestrians=traffic.pedestrians
        )
