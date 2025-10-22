from fastapi import FastAPI, status
from app.config import settings
from app.routers.cars import router as cars_router

app = FastAPI(title=settings.app_name)

@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {"status": "ok", "app": settings.app_name}

app.include_router(cars_router)