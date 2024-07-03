from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager

from app.application.commands.create_traffic_small import CreateTrafficSmall
from app.application.commands.get_traffic_small import GetTrafficSmall
from app.application.commands.get_traffics_small import GetTrafficsSmall
from app.application.commands.update_traffic_small import UpdateTrafficSmall


class TrafficSmallInteractorFactory(ABC):
    @abstractmethod
    def create_traffic(
            self
    ) -> AbstractAsyncContextManager[CreateTrafficSmall]: ...

    @abstractmethod
    def get_traffic(
            self
    ) -> AbstractAsyncContextManager[GetTrafficSmall]: ...

    @abstractmethod
    def get_traffics(
            self
    ) -> AbstractAsyncContextManager[GetTrafficsSmall]: ...

    @abstractmethod
    def update_traffic(
            self
    ) -> AbstractAsyncContextManager[UpdateTrafficSmall]: ...
