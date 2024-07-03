import uuid

from app.adapter.models import SmallTraffic
from app.application.protocols.repository_traffic_small import (
    ASmallTrafficRepository
)
from app.application.protocols.storage import AbstractStorage
from app.domain.models.traffic import TrafficSmall


class SmallTrafficRepository(ASmallTrafficRepository):
    def __init__(self, storage: AbstractStorage) -> None:
        self.storage = storage

    def add(self, traffic: TrafficSmall) -> SmallTraffic:
        traffic = SmallTraffic(
            status=traffic.status,
            pedestrians=traffic.pedestrians,
            large_traffic_id=traffic.large_traffic_id
        )
        result = self.storage.add(traffic, "small").correct_traffic_status()
        return result.get(traffic.id, "small")

    def update(self, traffic: TrafficSmall) -> SmallTraffic:
        traffic = SmallTraffic(
            id=traffic.id,
            status=traffic.status,
            pedestrians=traffic.pedestrians,
            large_traffic_id=traffic.large_traffic_id
        )
        result = self.storage.update(
            traffic, "small"
        ).correct_traffic_status()
        return result.get(traffic.id, "small")

    def get(self, traffic_id: uuid.UUID) -> SmallTraffic | None:
        return self.storage.correct_traffic_status().get(traffic_id, "small")

    def get_all(self) -> list[SmallTraffic]:
        return self.storage.correct_traffic_status().get_all("small")

    def delete(self, traffic_id: uuid.UUID) -> None:
        self.storage.delete(traffic_id, "small")
