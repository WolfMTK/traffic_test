import uuid
from typing import Literal

from app.domain.models.traffic import TrafficSmall


class TrafficSmallService:
    def create_traffic(
            self,
            status: Literal["GREEN", "RED"],
            pedestrians: int,
            large_traffic_id: uuid.UUID
    ) -> TrafficSmall:
        return TrafficSmall(
            status=status,
            pedestrians=pedestrians,
            large_traffic_id=large_traffic_id
        )

    def update_traffic(
            self,
            id: uuid.UUID,
            status: Literal["GREEN", "RED"] | None,
            pedestrians: int | None,
            large_traffic_id: uuid.UUID
    ) -> TrafficSmall:
        return TrafficSmall(
            id=id,
            status=status,
            pedestrians=pedestrians,
            large_traffic_id=large_traffic_id
        )

    def get_traffic(self, data: TrafficSmall | None) -> TrafficSmall:
        if data is None:
            raise ValueError("Traffic not found")
        return data

    def sort_status(self,
                    status: Literal["GREEN", "RED"],
                    data: list[TrafficSmall]) -> list[TrafficSmall]:
        if status is None:
            return data
        return [value for value in data
                if value.status.upper() == status.upper()]
