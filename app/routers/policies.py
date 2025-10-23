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
    """
    Create a new insurance policy for a specific car.

    Args:
        car_id (int): The ID of the car for which the policy is created.
        data (PolicyCreate): The policy data from the request body.
        session (AsyncSession): Database session dependency.

    Returns:
        PolicyRead: The created policy details.

    Raises:
        HTTPException: 404 if the car is not found,
                       409 if a duplicate policy exists,
                       500 for unexpected errors.
    """

    car = await session.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    exists_statement = select(InsurancePolicy).where(
        InsurancePolicy.car_id == car_id,
        InsurancePolicy.provider == data.provider,
        InsurancePolicy.policy_number == data.policy_number,
    )
    existing_policy = await session.scalar(exists_statement)
    if existing_policy:
        raise HTTPException(
            status_code=409,
            detail="A policy with this number and provider already exists for this car."
        )
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
    """
    Check if a car has a valid insurance policy on a specific date.

    Args:
        car_id (int): The ID of the car to check.
        date_str (str): The date to validate (format: YYYY-MM-DD).
        session (AsyncSession): Database session dependency.

    Returns:
        ValidityResponse: Object indicating if the car has valid insurance on the given date.

    Raises:
        HTTPException: 404 if the car is not found,
                       400 if the date format is invalid or out of allowed range.
    """
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