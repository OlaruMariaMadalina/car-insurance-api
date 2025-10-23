from fastapi import APIRouter, status
from app.config import settings

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/", status_code=status.HTTP_200_OK)
def health():
    """
    Health check endpoint.

    Returns a simple status message and the application name.
    Used for monitoring and verifying that the API is running.

    Returns:
        dict: A dictionary with status and app name.
    """
    return {"status": "ok", "app": settings.app_name}