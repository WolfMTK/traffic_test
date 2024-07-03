from abc import ABC, abstractmethod
from typing import Any, TypeVar, Self

ModelType = TypeVar("ModelType")


class AbstractStorage(ABC):
    @abstractmethod
    def get(self, *args: Any, **kwargs: Any) -> ModelType | None: ...

    @abstractmethod
    def get_all(self, *args: Any, **kwargs: Any) -> list[ModelType]: ...

    @abstractmethod
    def add(self, *args: Any, **kwargs: Any) -> Self: ...

    @abstractmethod
    def update(self, *args: Any, **kwargs: Any) -> Self: ...

    @abstractmethod
    def delete(self, *args: Any, **kwargs: Any) -> None: ...

    @abstractmethod
    def correct_traffic_status(self) -> Self: ...
