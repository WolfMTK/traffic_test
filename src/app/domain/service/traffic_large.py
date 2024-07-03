import uuid
from typing import Literal

from app.domain.models.traffic import TrafficLarge


class TrafficLargeService:
    def create_traffic(self,
                       status: Literal["GREEN", "YELLOW", "RED"],
                       autos: int) -> TrafficLarge:
        return TrafficLarge(
            status=status,
            autos=autos
        )

    def update_traffic(
            self,
            id: uuid.UUID,
            status: Literal["GREEN", "YELLOW", "RED"] | None,
            autos: int | None
    ) -> TrafficLarge:
        return TrafficLarge(
            id=id,
            status=status,
            autos=autos
        )

    def get_traffic(self, data: TrafficLarge | None) -> TrafficLarge:
        if data is None:
            raise ValueError("Traffic not found")
        return data

    def sort_status(self,
                    status: Literal["GREEN", "YELLOW", "RED"] | None,
                    data: list[TrafficLarge]) -> list[TrafficLarge]:
        if status is None:
            return data
        return [value for value in data
                if value.status.upper() == status.upper()]
