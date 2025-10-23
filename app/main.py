from fastapi import FastAPI, status
from app.config import settings
from app.routers.cars import router as cars_router
from app.routers.health import router as health_router
from app.routers.policies import router as policy_router 
from app.routers.claim import router as claim_router
from app.scheduler import scheduler_singleton
from contextlib import asynccontextmanager
from app.logging.logging_setup import setup_logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    scheduler_singleton.start()
    yield 
    scheduler_singleton.shutdown()

app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.include_router(health_router)

app.include_router(cars_router)

app.include_router(policy_router)

app.include_router(claim_router)