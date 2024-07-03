from dataclasses import dataclass


@dataclass
class StatusQuery:
    status: str | None
