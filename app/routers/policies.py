from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.db_deps import get_session
from app.models.car import Car
from app.models.policy import InsurancePolicy
from app.schemas.policy import PolicyCreate, PolicyRead

router = APIRouter(prefix="/api/cars", tags=["policies"])

@router.post("/{car_id}/policies", response_model=PolicyCreate, status_code=status.HTTP_201_CREATED)
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

    return PolicyRead(
        id=policy.id,
        car_id=policy.car_id,
        provider=policy.provider,
        policy_number=policy.policy_number,
        start_date=policy.start_date,
        end_date=policy.end_date,
    )