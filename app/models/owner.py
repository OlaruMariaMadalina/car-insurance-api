from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.car import Car 

class Owner(Base):
    """
    SQLAlchemy model for the 'owners' table.

    Represents a car owner with full name, email, and a list of owned cars.
    """
    __tablename__="owners"

    id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)

    cars: Mapped[list["Car"]] = relationship("Car", back_populates="owner", cascade="all, delete-orphan")