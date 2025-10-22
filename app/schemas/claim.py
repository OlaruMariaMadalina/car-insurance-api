from pydantic import BaseModel, Field, field_validator
from datetime import date

class ClaimCreate(BaseModel):
    claim_date: date
    description: str = Field(..., max_length=64)
    amount: float = Field(..., ge=0.01)
    
class ClaimRead(BaseModel):
    id: int
    car_id: int
    claim_date: date
    description: str
    amount: float
