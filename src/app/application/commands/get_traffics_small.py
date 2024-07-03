from app.application.dto.query import StatusQuery
from app.application.dto.traffic_small import TrafficSmallResultDTO
from app.application.protocols.interactor import Interactor
from app.application.protocols.repository_traffic_small import (
    ASmallTrafficRepository,
)
from app.domain.service.traffic_small import TrafficSmallService


class GetTrafficsSmall(Interactor[StatusQuery, list[TrafficSmallResultDTO]]):
    def __init__(self,
                 repository: ASmallTrafficRepository,
                 service: TrafficSmallService) -> None:
        self.repository = repository
        self.service = service

    async def __call__(
            self, data: StatusQuery
    ) -> list[TrafficSmallResultDTO]:
        traffics = self.repository.get_all()
        traffics = self.service.sort_status(data.status, traffics)
        return [TrafficSmallResultDTO(
            id=value.id,
            status=value.status,  # type: ignore
            pedestrians=value.pedestrians
        ) for value in traffics]
