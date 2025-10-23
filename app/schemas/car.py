from pydantic import BaseModel, RootModel
from app.schemas.owner import OwnerRead
from datetime import date
from decimal import Decimal

class CarRead(BaseModel):
    """
    Pydantic schema for reading car details, including owner information.
    """
    id: int
    identification_number: str
    make: str
    model: str
    year: int
    owner: OwnerRead

    class Config:
        from_attributes = True

class CarHistoryItem(BaseModel):
    """
    Pydantic schema representing a single event in a car's history.
    Can be either a policy or a claim, with relevant metadata.
    """
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
    """
    Pydantic root model for a list of car history items.
    Used as the response schema for car history endpoints.
    """
    pass