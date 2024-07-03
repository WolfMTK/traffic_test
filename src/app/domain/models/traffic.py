import uuid
from dataclasses import dataclass, field
from typing import Literal
from uuid import UUID


@dataclass(kw_only=True)
class TrafficSmall:
    id: UUID | None = field(default=None)
    status: Literal["GREEN", "RED"] | None = field(default=None)
    pedestrians: int | None = field(default=None)
    large_traffic_id: uuid.UUID


@dataclass(kw_only=True)
class TrafficLarge:
    id: UUID | None = field(default=None)
    status: Literal["GREEN", "YELLOW", "RED"] | None = field(default=None)
    autos: int | None = field(default=None)
    traffics_small: list[TrafficSmall] | None = field(default=None)
