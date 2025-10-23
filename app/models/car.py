from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.owner import Owner
    from app.models.policy import InsurancePolicy
    from app.models.claim import Claim

class Car(Base):
    """
    SQLAlchemy model for the 'cars' table.

    Represents a car entity with its identification number, make, model, year,
    owner, insurance policies, and claims.
    """
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    identification_number: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    make: Mapped[str] = mapped_column(String(64), nullable=False)
    model: Mapped[str] = mapped_column(String(64), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)

    owner_id: Mapped[int] = mapped_column(ForeignKey("owners.id", ondelete="CASCADE"))
    owner: Mapped["Owner"] = relationship("Owner", back_populates="cars")

    policies: Mapped[list["InsurancePolicy"]] = relationship("InsurancePolicy", back_populates="car")
    claims: Mapped[list["Claim"]] = relationship("Claim", back_populates="car")