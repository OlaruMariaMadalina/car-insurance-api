from pydantic import BaseModel, Field, field_validator
from datetime import date

class ClaimCreate(BaseModel):
    """
    Pydantic schema for creating a new insurance claim.

    Fields:
        claim_date (date): The date of the claim.
        description (str): Description of the claim (max 64 characters).
        amount (float): The claimed amount (must be positive).
    """
    claim_date: date
    description: str = Field(..., min_length=1, max_length=64)
    amount: float = Field(..., ge=0.01)
    
class ClaimRead(BaseModel):
    """
    Pydantic schema for reading insurance claim details.

    Fields:
        id (int): Unique identifier of the claim.
        car_id (int): Identifier of the car associated with the claim.
        claim_date (date): The date of the claim.
        description (str): Description of the claim.
        amount (float): The claimed amount.
    """
    id: int
    car_id: int
    claim_date: date
    description: str
    amount: float
