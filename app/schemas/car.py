from pydantic import BaseModel, Field
from typing import Literal, Annotated, Union
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

class PolicyHistoryItem(BaseModel):
    type: Literal["POLICY"] = "POLICY"
    policy_id: int
    start_date: date
    end_date: date
    provider: str

    class Config:
        populate_by_name = True
        from_attributes = True

class ClaimHistoryItem(BaseModel):
    type: Literal["CLAIM"] = "CLAIM"
    claim_id: int
    claim_date: date
    amount: Decimal
    description: str

    class Config:
        populate_by_name = True
        from_attributes = True

HistoryItem = Annotated[Union[PolicyHistoryItem, ClaimHistoryItem], Field(discriminator="type")]