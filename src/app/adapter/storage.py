import uuid
from typing import Any, Self, Literal

from app.adapter.models import SmallTraffic, LargeTraffic
from app.application.protocols.storage import AbstractStorage

ZERO = 0
TRAFFIC = 4
LIMIT_SMALL_TRAFFIC = 2
LIMIT_LARGE_TRAFFIC = 4


# Сделал реализацию без использования БД, но с ней было бы легче
class MemoryStorageTraffic(AbstractStorage):
    _storage: dict[str, list[SmallTraffic | LargeTraffic] | int | str] = {
        "traffic_small": [],
        "traffic_large": [],
        "timer": 0,
        "is_green": True,
        "is_yellow": True,
    }

    def __new__(cls, *args: Any, **kwargs: Any) -> "MemoryStorageTraffic":
        # Singleton используется для хранения,
        # есть и другие варианты, как можно было реализовать хранение данных
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance  # type: ignore

    def get(
            self,
            traffic_id: uuid.UUID,
            tag: Literal["small", "large"]
    ) -> SmallTraffic | LargeTraffic | None:
        if tag == "small":
            stack = self._storage["traffic_small"]
            return self._get_traffic(stack, traffic_id)
        elif tag == "large":
            stack = self._storage["traffic_large"]
            return self._get_traffic(stack, traffic_id)
        raise ValueError("Something went wrong")

    def get_all(
            self,
            tag: Literal["small", "large"]
    ) -> list[SmallTraffic | LargeTraffic]:
        if tag == "small":
            return self._storage["traffic_small"]
        elif tag == "large":
            return self._storage["traffic_large"]
        raise ValueError("Something went wrong")

    def add(self,
            traffic: SmallTraffic | LargeTraffic,
            tag: Literal["small", "large"]) -> Self:
        match tag:
            case "small":
                stack = self._storage["traffic_small"]
                self._add_traffic_small(stack, traffic)
            case "large":
                stack = self._storage["traffic_large"]
                self._add_traffic_large(stack, traffic)
            case _:
                raise ValueError("Something went wrong")
        return self

    def update(self,
               traffic: SmallTraffic | LargeTraffic,
               tag: Literal["small", "large"]) -> Self:
        match tag:
            case "small":
                stack = self._storage["traffic_small"]
                self._update_traffic_small(stack, traffic)
            case "large":
                stack = self._storage["traffic_large"]
                self._update_traffic_large(stack, traffic)
            case _:
                raise ValueError("Something went wrong")
        return self

    def delete(self,
               traffic_id: uuid.UUID,
               tag: Literal["small", "large"]) -> Self:
        if tag == "small":
            self._del_traffic_small(traffic_id)
            return self
        elif tag == "large":
            self._del_traffic_large(traffic_id)
            return self
        raise ValueError("Something went wrong")

    def correct_traffic_status(self) -> Self:
        if self._storage["timer"] > ZERO:
            self._storage["timer"] -= 1
            return self
        self._correct_traffic_status()
        return self

    def _correct_traffic_status(self) -> None:
        # Возможно не идеальный алгоритм, но в основном корректировка
        # состояния происходит в данном коде
        # (можно было разбить на несколько методов)
        stack_traffic_large = self._storage["traffic_large"]
        stack_traffic_small = self._storage["traffic_small"]
        if self._storage["is_yellow"]:
            self._storage["is_yellow"] = False
            self._storage["timer"] = 15

            if self._storage["is_green"]:
                even_stack = stack_traffic_large[::2]
                odd_stack = stack_traffic_large[1::2]
                self._storage["is_green"] = False
            else:
                even_stack = stack_traffic_large[1::2]
                odd_stack = stack_traffic_large[::2]
                self._storage["is_green"] = True

            for traffic in even_stack:
                traffic.status = "GREEN"
                for value in traffic.traffics_small:
                    value.status = "RED"

            for traffic in odd_stack:
                traffic.status = "RED"
                for value in traffic.traffics_small:
                    value.status = "GREEN"

            for value in stack_traffic_small:
                if value.id in even_stack:
                    value.status = "RED"
                if value.id in odd_stack:
                    value.status = "GREEN"
        else:
            self._set_yellow()
            self._storage["is_yellow"] = True

    def _set_yellow(self):
        self._storage["timer"] = 5
        traffic = self._storage["traffic_large"]
        for value in traffic:
            value.status = "YELLOW"

    def _update_traffic_small(self,
                              stack: list[SmallTraffic],
                              traffic: SmallTraffic) -> None:
        if len(stack) == ZERO:
            raise ValueError("Traffic not found")

        if not self._check_traffic_large(traffic.large_traffic_id):
            raise ValueError("ID traffic large not found")

        self._update_value(stack, traffic)

        traffic_large = self.get(traffic.large_traffic_id, "large")
        for index in range(len(traffic_large.traffics_small)):
            if traffic_large.traffics_small[index].id == traffic.id:
                traffic_large.traffics_small[index] = traffic

        self._update_value(self._storage["traffic_large"], traffic_large)

    def _update_traffic_large(self,
                              stack: list[LargeTraffic],
                              traffic: LargeTraffic) -> None:
        if len(stack) == ZERO:
            raise ValueError("Traffic not found")

        self._update_value(stack, traffic)

    def _get_traffic(
            self,
            stack: list[SmallTraffic] | list[LargeTraffic],
            traffic_id: uuid.UUID
    ) -> SmallTraffic | LargeTraffic | None:
        for value in stack:
            if value.id == traffic_id:
                return value

    def _del_traffic_large(self, traffic_id: uuid.UUID) -> None:
        stack_traffic_small = self._storage["traffic_small"]
        stack_traffic_large = self._storage["traffic_large"]

        self._storage["traffic_small"] = [
            value for value in stack_traffic_small
            if value.large_traffic_id != traffic_id
        ]

        for index, value in enumerate(stack_traffic_large):
            if value.id == traffic_id:
                stack_traffic_large.pop(index)
                break

    def _del_traffic_small(
            self,
            traffic_id: uuid.UUID
    ) -> None:
        stack_traffic_small = self._storage["traffic_small"]
        stack_traffic_large = self._storage["traffic_large"]

        for index, value in enumerate(stack_traffic_small):
            if value.id == traffic_id:
                stack_traffic_small.pop(index)
                break

        for traffic in stack_traffic_large:
            for index, value in enumerate(traffic.traffics_small):
                if value.id == traffic_id:
                    traffic.traffics_small.pop(index)
                    break

    def _add_traffic_small(self,
                           stack: list[SmallTraffic],
                           traffic: SmallTraffic) -> None:
        if not self._check_traffic_large(traffic.large_traffic_id):
            raise ValueError("ID traffic large not found")

        traffic_large = self.get(traffic.large_traffic_id, "large")
        if len(traffic_large.traffics_small) == LIMIT_SMALL_TRAFFIC:
            raise ValueError("Number of traffic lights exceeded")

        traffic_large.traffics_small.append(traffic)

        if traffic.status == "YELLOW":
            self._set_yellow()

        self._add_value(stack, traffic)
        self._update_value(self._storage["traffic_large"], traffic_large)

    def _check_traffic_large(self, traffic_id: uuid.UUID) -> bool:
        stack = self._storage['traffic_large']
        for value in stack:
            if value.id == traffic_id:
                return True
        return False

    def _add_traffic_large(self,
                           stack: list[LargeTraffic],
                           traffic: LargeTraffic) -> Self:
        if len(stack) == ZERO:
            stack.append(traffic)
            return self

        if len(stack) == LIMIT_LARGE_TRAFFIC:
            raise ValueError("Number of traffic lights exceeded")

        if traffic.status == "YELLOW":
            self._set_yellow()

        self._check_traffic_length(traffic)
        self._add_value(stack, traffic)

    def _check_traffic_length(self, traffic):
        if len(traffic.traffics_small) > 2:
            raise ValueError("The wrong number of small traffic lights")

    def _add_value(self,
                   stack: list[SmallTraffic | LargeTraffic],
                   traffic: SmallTraffic | LargeTraffic) -> None:
        for value in stack:
            if value.id == traffic.id:
                raise ValueError("The data is already available in the repository")
        if traffic.status != "YELLOW":
            self._storage["timer"] = ZERO
        stack.append(traffic)

    def _update_value(self,
                      stack: list[SmallTraffic | LargeTraffic],
                      traffic: SmallTraffic | LargeTraffic) -> None:
        keys = tuple(vars(traffic).keys())
        for value in stack:
            if value.id == traffic.id:
                self._set_values(value, traffic, keys)
                return
        raise ValueError("Traffic not found")

    def _set_values(self,
                    _kw: SmallTraffic | LargeTraffic,
                    traffic: SmallTraffic | LargeTraffic,
                    keys: tuple[str, ...]) -> None:
        if traffic.status is not None and traffic.status != "YELLOW":
            self._storage["timer"] = ZERO
        for key in keys:
            value = getattr(traffic, key)
            if value is None or key == "traffics_small":
                continue
            setattr(_kw, key, value)
