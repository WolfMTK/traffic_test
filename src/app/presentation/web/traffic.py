import uuid

from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.application.commands import (
    update_traffic_large as command_update_traffic_large
)
from app.application.commands.create_traffic_small import (
    TrafficSmallCreateDTO as TrafficSmallCreate
)
from app.application.commands.update_traffic_small import (
    TrafficSmallUpdateDTO as TrafficSmallUpdate
)
from app.application.dto.query import StatusQuery
from app.application.dto.traffic_large import (
    TrafficLargeResultDTO,
    TrafficLargeCreateDTO,
    TrafficLargeUpdateDTO
)
from app.application.dto.traffic_small import TrafficSmallCreateDTO, TrafficSmallUpdateDTO, TrafficSmallResultDTO
from app.presentation.traffic_large_interactor import (
    TrafficLargeInteractorFactory
)
from app.presentation.traffic_small_interactor import TrafficSmallInteractorFactory

traffic_router = APIRouter(prefix="/traffic", tags=["traffic"])


@traffic_router.post(
    "/large",
    response_model=TrafficLargeResultDTO
)
async def create_traffic_large(
        traffic: TrafficLargeCreateDTO,
        ioc: TrafficLargeInteractorFactory = Depends()
):
    """
    Создание светофоров, регулирующих автомобили

    **status** - светофор может принимать три статуса: зеленый, желтый, красный

    **autos** - количество автомобилей

    Результат будет скорректирован с другими светофорами, которые имеются в стеке.
    """
    try:
        async with ioc.create_traffic() as create_traffic_factory:
            return await create_traffic_factory(traffic)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )


@traffic_router.put(
    "/large/{id}",
    response_model=TrafficLargeResultDTO
)
async def update_traffic_large(
        id: uuid.UUID,
        traffic: TrafficLargeUpdateDTO,
        ioc: TrafficLargeInteractorFactory = Depends()
):
    """
    Обновление светофоров, регулирующих автомобили

    **status** - светофор может принимать три статуса:
    зеленый, желтый, красный

    **autos** - количество автомобилей

    Результат будет скорректирован с другими светофорами,
    которые имеются в стеке.
    """
    try:
        async with ioc.update_traffic() as update_traffic_factory:
            traffic = command_update_traffic_large.TrafficLargeUpdateDTO(
                id=id,
                status=traffic.status,
                autos=traffic.autos
            )
            return await update_traffic_factory(traffic)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )


@traffic_router.get(
    "/large",
    response_model=list[TrafficLargeResultDTO]
)
async def get_traffics_large(
        traffic_status: str | None = Query(None),
        ioc: TrafficLargeInteractorFactory = Depends()
):
    """
    Получение всех светофоров, регулирующих автомобили

    При вводе параметра **traffic_status** будет доступна сортировка
    """
    try:
        async with ioc.get_traffics() as get_traffics_factory:
            return await get_traffics_factory(StatusQuery(traffic_status))
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )


@traffic_router.get(
    "/large/{id}",
    response_model=TrafficLargeResultDTO
)
async def get_traffic_large(
        id: uuid.UUID,
        ioc: TrafficLargeInteractorFactory = Depends()
):
    """
    Получение светофора, регулирующего автомобили, по его идентификатору
    """
    try:
        async with ioc.get_traffic() as get_traffic_factory:
            return await get_traffic_factory(id)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )


@traffic_router.post(
    "/small/{id}",
    response_model=TrafficSmallResultDTO
)
async def create_traffic_small(
        id: uuid.UUID,
        traffic: TrafficSmallCreateDTO,
        ioc: TrafficSmallInteractorFactory = Depends()
):
    """
    Создание светофора, регулирующий движение пешеходов

    **id** - уникальный идентификатор светофора, регулирующий автомобили

    **status** - светофор может принимать два статуса: зеленый, красный

    **pedestrians** - количество пешеходов
    """
    try:
        async with ioc.create_traffic() as create_traffic_factory:
            return await create_traffic_factory(
                TrafficSmallCreate(
                    id=id,
                    status=traffic.status,
                    pedestrians=traffic.pedestrians
                )
            )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )


@traffic_router.put(
    "/small/{id}",
    response_model=TrafficSmallResultDTO
)
async def update_traffic_small(
        id: uuid.UUID,
        traffic: TrafficSmallUpdateDTO,
        ioc: TrafficSmallInteractorFactory = Depends()
):
    """
        Обновление светофора, регулирующий движение пешеходов

        **id** - уникальный идентификатор светофора,
        регулирующий движение пешеходов

        **status** - светофор может принимать два статуса: зеленый, красный

        **pedestrians** - количество пешеходов
    """
    try:
        async with ioc.update_traffic() as update_traffic_factory:
            return await update_traffic_factory(
                TrafficSmallUpdate(
                    id=id,
                    status=traffic.status,
                    pedestrians=traffic.pedestrians
                )
            )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )


@traffic_router.get(
    "/small/{id}",
    response_model=TrafficSmallResultDTO
)
async def get_traffic_small(
        id: uuid.UUID,
        ioc: TrafficSmallInteractorFactory = Depends()
):
    """Получение светофора, регулирующий движение пешеходов,
     по его идентификатору"""
    try:
        async with ioc.get_traffic() as get_traffic_factory:
            return await get_traffic_factory(id)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )


@traffic_router.get(
    "/small",
    response_model=list[TrafficSmallResultDTO]
)
async def get_traffics_small(
        traffic_status: str | None = Query(None),
        ioc: TrafficSmallInteractorFactory = Depends()
):
    """
    Получение светофоров, регулирующих движение пешеходов

    При вводе параметра **traffic_status** будет доступна сортировка
    """
    try:
        async with ioc.get_traffics() as get_traffics_factory:
            return await get_traffics_factory(StatusQuery(traffic_status))
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )
