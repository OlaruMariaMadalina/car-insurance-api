from fastapi import APIRouter, Depends, HTTPException, Path, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.utils.db_deps import get_session
from app.models.car import Car
from app.models.policy import InsurancePolicy
from app.schemas.policy import PolicyCreate, PolicyRead, ValidityResponse
from datetime import date
import structlog

log = structlog.get_logger()

router = APIRouter(prefix="/api/cars", tags=["policies"])

@router.post("/{car_id}/policies", response_model=PolicyRead, status_code=status.HTTP_201_CREATED)
async def create_policy(
    car_id: int = Path(..., ge=1),
    data: PolicyCreate | None=None,
    session: AsyncSession = Depends(get_session),
):
    car = await session.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    policy = InsurancePolicy(
        car_id=car_id,
        provider=data.provider,
        policy_number=data.policy_number,
        start_date=data.start_date,
        end_date=data.end_date,
    )
    session.add(policy)
    await session.flush()
    await session.commit()
    
    log.info("policy_created",
         policy_id=policy.id, car_id=policy.car_id,
         provider=policy.provider, start=str(policy.start_date), end=str(policy.end_date))

    return PolicyRead(
        id=policy.id,
        car_id=policy.car_id,
        provider=policy.provider,
        policy_number=policy.policy_number,
        start_date=policy.start_date,
        end_date=policy.end_date,
    )

@router.get("/{car_id}/insurance-valid",response_model=ValidityResponse, status_code=status.HTTP_200_OK)
async def check_insurance_validity(
    car_id: int = Path(..., ge=1),
    date_str: str = Query(..., alias="date"),
    session: AsyncSession = Depends(get_session)
):
    car = await session.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    
    try:
        validation_date = date.fromisoformat(date_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Expected YYYY-MM-DD")
    if validation_date.year < 1900 or validation_date.year > 2100:
        raise HTTPException(status_code=400, detail="Date out of allowed range (1900-2100).")
    
    statement = select(func.count()).select_from(InsurancePolicy).where(
        InsurancePolicy.car_id == car_id,
        InsurancePolicy.start_date <= validation_date,
        InsurancePolicy.end_date >= validation_date,
    )

    count = await session.scalar(statement)

    is_valid = count and count > 0

    return ValidityResponse(car_id=car_id, date=validation_date.isoformat(), valid=bool(is_valid))