from fastapi import APIRouter, Depends, HTTPException, Path, status, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.utils.db_deps import get_session
from app.models.car import Car
from app.models.claim import Claim
from app.schemas.claim import ClaimRead, ClaimCreate
from datetime import date
import structlog

log = structlog.get_logger()

router = APIRouter(prefix="/api/cars", tags=["policies"])

@router.post("/{car_id}/claims", response_model=ClaimRead, status_code=status.HTTP_201_CREATED)
async def create_claim(
    data: ClaimCreate,
    response: Response,
    car_id: int = Path(..., ge=1),
    session: AsyncSession = Depends(get_session),
):
    """
    Create a new insurance claim for a specific car.

    Args:
        data (ClaimCreate): The claim data from the request body.
        response (Response): FastAPI response object for setting headers.
        car_id (int): The ID of the car for which the claim is created.
        session (AsyncSession): Database session dependency.

    Returns:
        ClaimRead: The created claim details.

    Raises:
        HTTPException: 404 if the car is not found, 500 for unexpected errors.
    """
    car = await session.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    claim = Claim(
        car_id=car_id,
        claim_date=data.claim_date,
        description=data.description,
        amount=data.amount,
    )
    session.add(claim)
    await session.flush()
    await session.commit()

    response.headers["Location"] = f"/api/cars/{car_id}/claims/{claim.id}"

    log.info("claim_created",
        claim_id=claim.id, car_id=claim.car_id,
        amount=str(claim.amount), claim_date=str(claim.claim_date))
    
    return ClaimRead(
        id=claim.id,
        car_id=claim.car_id,
        claim_date=claim.claim_date,
        description=claim.description,
        amount=claim.amount,
    )
