from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager

from app.application.commands.create_traffic_large import CreateTrafficLarge
from app.application.commands.get_traffic_large import GetTrafficLarge
from app.application.commands.get_traffics_large import GetTrafficsLarge
from app.application.commands.update_traffic_large import UpdateTrafficLarge


class TrafficLargeInteractorFactory(ABC):
    @abstractmethod
    def create_traffic(
            self
    ) -> AbstractAsyncContextManager[CreateTrafficLarge]: ...

    @abstractmethod
    def update_traffic(
            self
    ) -> AbstractAsyncContextManager[UpdateTrafficLarge]: ...

    @abstractmethod
    def get_traffics(
            self
    ) -> AbstractAsyncContextManager[GetTrafficsLarge]: ...

    @abstractmethod
    def get_traffic(
            self
    ) -> AbstractAsyncContextManager[GetTrafficLarge]: ...
