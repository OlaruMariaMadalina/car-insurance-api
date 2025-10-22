from fastapi import FastAPI, status
from app.config import settings
from app.routers.cars import router as cars_router
from app.routers.health import router as health_router
from app.routers.policies import router as policy_router 

app = FastAPI(title=settings.app_name)

app.include_router(health_router)

app.include_router(cars_router)

app.include_router(policy_router)