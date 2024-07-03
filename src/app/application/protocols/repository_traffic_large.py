import uuid
from abc import ABC, abstractmethod
from typing import TypeVar

ModelType = TypeVar("ModelType")


class ALargeTrafficRepository(ABC):
    @abstractmethod
    def add(self, traffic: ModelType) -> ModelType: ...

    @abstractmethod
    def update(self, traffic: ModelType) -> ModelType: ...

    @abstractmethod
    def get(self, id: uuid.UUID) -> ModelType | None: ...

    @abstractmethod
    def get_all(self) -> list[ModelType]: ...

    @abstractmethod
    def delete(self, id: uuid.UUID) -> None: ...
