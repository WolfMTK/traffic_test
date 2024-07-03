from fastapi import FastAPI, Depends

from app.adapter.repository_traffic_large import LargeTrafficRepository
from app.adapter.repository_traffic_small import SmallTrafficRepository
from app.adapter.storage import MemoryStorageTraffic
from app.application.protocols.repository_traffic_large import (
    ALargeTrafficRepository,
)
from app.application.protocols.repository_traffic_small import (
    ASmallTrafficRepository,
)
from app.application.protocols.storage import AbstractStorage


def new_storage():
    return MemoryStorageTraffic()


def new_repository_traffic_large(storage: AbstractStorage = Depends()):
    return LargeTrafficRepository(storage)


def new_repository_traffic_small(storage: AbstractStorage = Depends()):
    return SmallTrafficRepository(storage)


def init_depends(app: FastAPI) -> None:
    app.dependency_overrides.update({
        AbstractStorage: new_storage,
        ALargeTrafficRepository: new_repository_traffic_large,
        ASmallTrafficRepository: new_repository_traffic_small
    })
