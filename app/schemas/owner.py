from pydantic import BaseModel, EmailStr

class OwnerRead(BaseModel):
    id: int
    full_name: str
    email: EmailStr

    class Config:
        from_attributes = True