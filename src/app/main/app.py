from fastapi import FastAPI

from app.adapter.di import init_depends
from app.main.ioc import TrafficLargeIOC, TrafficSmallIOC
from app.presentation.traffic_large_interactor import TrafficLargeInteractorFactory
from app.presentation.traffic_small_interactor import TrafficSmallInteractorFactory
from app.presentation.web import traffic


def start_app() -> FastAPI:
    app = FastAPI()
    app.include_router(traffic.traffic_router)

    init_depends(app)
    app.dependency_overrides.update({
        TrafficLargeInteractorFactory: TrafficLargeIOC,
        TrafficSmallInteractorFactory: TrafficSmallIOC
    })
    return app
