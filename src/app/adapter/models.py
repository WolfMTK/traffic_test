import uuid
from dataclasses import dataclass
from typing import Any

from app.domain.models.traffic import TrafficSmall, TrafficLarge


@dataclass(kw_only=True)
class SmallTraffic(TrafficSmall):
    def __post_init__(self) -> None:
        if self.id is None:
            self.id = uuid.uuid4()

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "status": self.status,
            "pedestrians": self.pedestrians
        }


@dataclass(kw_only=True)
class LargeTraffic(TrafficLarge):
    def __post_init__(self) -> None:
        if self.id is None:
            self.id = uuid.uuid4()
        if self.traffics_small is None:
            self.traffics_small = []

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "status": self.status,
            "autos": self.autos,
            "traffics_light": self.traffics_small
        }
