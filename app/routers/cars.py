# app/main.py
from fastapi import Depends, Query, status, APIRouter, Path, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.db_deps import get_session
from app.config import settings
from app.schemas.car import CarRead, HistoryItem, PolicyHistoryItem, ClaimHistoryItem
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
    """
    Returns a paginated list of cars and their owners.

    Args:
        session (AsyncSession): Database session dependency.
        limit (int): Maximum number of cars to return (default: 50).
        offset (int): Number of cars to skip (default: 0).

    Returns:
        List[CarRead]: List of car details with owner information.
    """
    statement = (
        select(Car)
        .options(selectinload(Car.owner))
        .order_by(Car.id).limit(limit).offset(offset)
    )

    cars = (await session.execute(statement)).scalars().all()

    car_reads = [CarRead.model_validate(c) for c in cars]
    return car_reads


@router.get("/{car_id}/history", response_model=list[HistoryItem], status_code=status.HTTP_200_OK)
async def get_car_history(
    session: AsyncSession = Depends(get_session),
    car_id: int = Path(..., ge=1)
):
    """
    Returns the chronological history of a car, including all insurance policies and claims.

    Args:
        session (AsyncSession): Database session dependency.
        car_id (int): The ID of the car for which to retrieve history.

    Returns:
        List[CarHistoryItem]: List of events (policies and claims) for the car.
    """
    car = await session.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    policy_statement = select(InsurancePolicy).where(InsurancePolicy.car_id == car.id)
    policy_response = await session.execute(policy_statement)
    policies = policy_response.scalars().all()

    claim_statement = select(Claim).where(Claim.car_id == car.id)
    claim_response = await session.execute(claim_statement)
    claims = claim_response.scalars().all()

    events: list[HistoryItem] = []

    for p in policies:
        events.append(
            PolicyHistoryItem(
                type="POLICY",
                policy_id=p.id,
                start_date=p.start_date,
                end_date=p.end_date,
                provider=p.provider,
            )
        )

    for c in claims:
        events.append(
            ClaimHistoryItem(
                type="CLAIM",
                claim_id=c.id,
                claim_date=c.claim_date,
                amount=c.amount,
                description=c.description,
            )
        )
        
    events.sort(
        key=lambda item: getattr(item, "start_date", None) or getattr(item, "claim_date", None) or getattr(item, "end_date", None)
    )
    
    return [e.model_dump(by_alias=True, exclude_none=True) for e in events]