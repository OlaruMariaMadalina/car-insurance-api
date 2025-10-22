from pydantic import BaseModel, RootModel
from app.schemas.owner import OwnerRead
from datetime import date
from decimal import Decimal

class CarRead(BaseModel):
    id: int
    identification_number: str
    make: str
    model: str
    year: int
    owner: OwnerRead

    class Config:
        from_attributes = True

class CarHistoryItem(BaseModel):
    type:str
    policy_id: int | None = None
    start_date: date | None = None
    end_date: date | None = None
    provider: str | None = None

    claim_id: int | None = None
    claim_date: date | None = None
    amount: Decimal | None = None
    description: str | None = None

class CarHistoryResponse(RootModel[list[CarHistoryItem]]):
    pass