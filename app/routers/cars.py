# app/main.py
from fastapi import FastAPI, Depends, Query, status, APIRouter, Path, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.db_deps import get_session
from app.config import settings
from app.schemas.car import CarRead, CarHistoryItem
from sqlalchemy import select
from app.models.car import Car
from app.models.policy import InsurancePolicy
from app.models.claim import Claim

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

@router.get("/{car_id}/history", response_model=list[CarHistoryItem], status_code=status.HTTP_200_OK)
async def get_car_history(
    session: AsyncSession = Depends(get_session),
    car_id: int = Path(..., ge=1)
):
    car = await session.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    policy_statement = select(InsurancePolicy).where(InsurancePolicy.car_id == car.id)
    policy_response = await session.execute(policy_statement)
    policies = policy_response.scalars().all()

    claim_statement = select(Claim).where(Claim.car_id == car.id)
    claim_response = await session.execute(claim_statement)
    claims = claim_response.scalars().all()

    events: list[CarHistoryItem] = []

    for p in policies:
        events.append(
            CarHistoryItem(
                type="POLICY",
                policy_id=p.id,
                start_date=p.start_date,
                end_date=p.end_date,
                provider=p.provider,
            )
        )

    for c in claims:
        events.append(
            CarHistoryItem(
                type="CLAIM",
                policy_id=c.id,
                claim_date=c.claim_date,
                amount=c.amount,
                description=c.description,
            )
        )
    events.sort(
        key=lambda item: item.start_date or item.claim_date or item.end_date
    )
    
    return events