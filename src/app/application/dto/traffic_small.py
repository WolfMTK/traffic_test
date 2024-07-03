import uuid
from dataclasses import dataclass, field
from typing import Literal


@dataclass
class TrafficSmallCreateDTO:
    status: Literal["GREEN", "RED"]
    pedestrians: int


@dataclass
class TrafficSmallResultDTO:
    id: uuid.UUID
    status: Literal["GREEN", "RED"]
    pedestrians: int


@dataclass
class TrafficSmallUpdateDTO:
    status: Literal["GREEN", "RED"] | None = field(default=None)
    pedestrians: int | None = field(default=None)
