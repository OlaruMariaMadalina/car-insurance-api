from pydantic import BaseModel, Field, field_validator
from datetime import date

class PolicyCreate(BaseModel):
    provider: str
    policy_number: str = Field(..., max_length=64)
    start_date: date
    end_date: date

    @field_validator("end_date")
    @classmethod
    def end_after_start(cls, v:date, info):
        start = info.data.get("start_date")
        if start and v < start:
            raise ValueError("end-date must be greater than start_date")
        return v
    
class PolicyRead(BaseModel):
    id: int
    car_id: int
    provider: str
    policy_number: str
    start_date: date
    end_date: date