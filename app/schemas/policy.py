from pydantic import BaseModel, Field, field_validator
from datetime import date

class PolicyCreate(BaseModel):
    """
    Pydantic schema for creating a new insurance policy.

    Fields:
        provider (str): Name of the insurance provider.
        policy_number (str): Policy number (max 64 characters).
        start_date (date): Start date of the policy.
        end_date (date): End date of the policy (must be after start_date).
    """
    provider: str
    policy_number: str = Field(..., max_length=64)
    start_date: date
    end_date: date

    @field_validator("end_date")
    @classmethod
    def end_after_start(cls, v:date, info):
        """
        Validator to ensure end_date is after start_date.
        Raises ValueError if not.
        """
        start = info.data.get("start_date")
        if start and v < start:
            raise ValueError("end-date must be greater than start_date")
        return v
    
class PolicyRead(BaseModel):
    """
    Pydantic schema for reading insurance policy details.

    Fields:
        id (int): Unique identifier of the policy.
        car_id (int): Identifier of the car associated with the policy.
        provider (str): Name of the insurance provider.
        policy_number (str): Policy number.
        start_date (date): Start date of the policy.
        end_date (date): End date of the policy.
    """
    id: int
    car_id: int
    provider: str
    policy_number: str
    start_date: date
    end_date: date

class ValidityResponse(BaseModel):
    """
    Pydantic schema for the insurance validity response.

    Fields:
        car_id (int): Identifier of the car.
        date (date): Date for which validity is checked.
        valid (bool): Whether the car has valid insurance on the given date.
    """
    car_id: int
    date: date
    valid: bool