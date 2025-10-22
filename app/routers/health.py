from fastapi import APIRouter, status
from app.config import settings

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/", status_code=status.HTTP_200_OK)
def health():
    return {"status": "ok", "app": settings.app_name}