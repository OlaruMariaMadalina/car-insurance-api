from pydantic import BaseModel, EmailStr

class OwnerRead(BaseModel):
    """
    Pydantic schema for reading owner details.

    Fields:
        id (int): Unique identifier of the owner.
        full_name (str): Full name of the owner.
        email (EmailStr): Email address of the owner.
    """
    id: int
    full_name: str
    email: EmailStr

    class Config:
        from_attributes = True