from pydantic import BaseModel
from app.schemas.owner import OwnerRead

class CarRead(BaseModel):
    id: int
    identification_number: str
    make: str
    model: str
    year: int
    owner: OwnerRead

    class Config:
        from_attributes = True