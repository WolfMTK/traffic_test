import uuid
from dataclasses import dataclass, field
from typing import Literal

from app.application.dto.traffic_large import TrafficLargeResultDTO
from app.application.protocols.interactor import Interactor
from app.application.protocols.repository_traffic_large import (
    ALargeTrafficRepository,
)
from app.domain.service.traffic_large import TrafficLargeService


@dataclass
class TrafficLargeUpdateDTO:
    id: uuid.UUID
    status: Literal["GREEN", "YELLOW", "RED"] | None = field(default=None)
    autos: int | None = field(default=None)


class UpdateTrafficLarge(
    Interactor[TrafficLargeUpdateDTO, TrafficLargeResultDTO]
):
    def __init__(self,
                 repository: ALargeTrafficRepository,
                 service: TrafficLargeService):
        self.repository = repository
        self.service = service

    async def __call__(
            self, data: TrafficLargeUpdateDTO
    ) -> TrafficLargeResultDTO:
        traffic = self.service.update_traffic(
            data.id, data.status, data.autos
        )
        traffic = self.repository.update(traffic)
        return TrafficLargeResultDTO(
            id=traffic.id,
            status=traffic.status,  # type: ignore
            autos=traffic.autos,
            traffics_small=traffic.traffics_small
        )
