import uuid
from dataclasses import dataclass, field
from typing import Literal

from app.domain.models.traffic import TrafficSmall


@dataclass
class TrafficLargeCreateDTO:
    status: Literal["GREEN", "YELLOW", "RED"]
    autos: int


@dataclass
class TrafficLargeResultDTO:
    id: uuid.UUID
    status: str
    autos: int
    traffics_small: list[TrafficSmall]


@dataclass
class TrafficLargeUpdateDTO:
    status: Literal["GREEN", "YELLOW", "RED"] | None = field(default=None)
    autos: int | None = field(default=None)
