# app/main.py
from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.db_deps import get_session
from app.config import settings

app = FastAPI(title=settings.app_name)

@app.get("/health")
async def health():
    return {"status": "ok", "app": settings.app_name}

@app.get("/health/db")
async def health_db(session: AsyncSession = Depends(get_session)):
    # Quick connectivity check
    await session.execute(text("SELECT 1"))
    return {"status": "ok", "db": "connected"}
