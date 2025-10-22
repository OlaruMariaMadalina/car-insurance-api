# app/main.py
from fastapi import FastAPI, Depends, Query, status, APIRouter
from sqlalchemy import text
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.db_deps import get_session
from app.config import settings
from app.schemas.car import CarRead
from sqlalchemy import select
from app.models.car import Car

router = APIRouter(prefix="/api/cars", tags=["cars"])

@router.get("", response_model=list[CarRead], status_code=status.HTTP_200_OK)
async def list_cars(
    session: AsyncSession = Depends(get_session),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0)
):
    statement = (
        select(Car)
        .options(selectinload(Car.owner))
        .order_by(Car.id).limit(limit).offset(offset)
    )

    cars = (await session.execute(statement)).scalars().all()

    car_reads = [CarRead.model_validate(c) for c in cars]
    return car_reads

