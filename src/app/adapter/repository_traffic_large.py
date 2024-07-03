import uuid

from app.adapter.models import LargeTraffic
from app.application.protocols.repository_traffic_large import (
    ALargeTrafficRepository
)
from app.application.protocols.storage import AbstractStorage
from app.domain.models.traffic import TrafficLarge


class LargeTrafficRepository(ALargeTrafficRepository):
    # Репозиторий должен был быть без инициализатора,
    # реализация всё же ближе к Gateway
    def __init__(self, storage: AbstractStorage) -> None:
        self.storage = storage

    def add(self, traffic: TrafficLarge) -> LargeTraffic:
        traffic = LargeTraffic(
            status=traffic.status,
            autos=traffic.autos
        )
        result = self.storage.add(traffic, "large").correct_traffic_status()
        return result.get(traffic.id, "large")

    def update(self, traffic: TrafficLarge) -> LargeTraffic:
        traffic = LargeTraffic(
            id=traffic.id,
            status=traffic.status,
            autos=traffic.autos
        )
        result = self.storage.update(
            traffic, "large"
        ).correct_traffic_status()
        return result.get(traffic.id, "large")

    def get(self, traffic_id: uuid.UUID) -> LargeTraffic | None:
        return self.storage.correct_traffic_status().get(traffic_id, "large")

    def get_all(self) -> list[TrafficLarge]:
        return self.storage.correct_traffic_status().get_all("large")

    def delete(self, traffic_id: uuid.UUID) -> None:
        self.storage.delete(traffic_id, "large")
