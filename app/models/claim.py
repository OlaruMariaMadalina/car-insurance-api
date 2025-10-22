from sqlalchemy import String, Integer, Date, DECIMAL, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.car import Car
from sqlalchemy import TIMESTAMP, func
from datetime import datetime

class Claim(Base):
    __tablename__ = "claims"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    claim_date: Mapped[Date] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(DECIMAL(12, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id", ondelete="CASCADE"))
    car: Mapped["Car"] = relationship("Car", back_populates="claims")

    __table_args__ = (
        CheckConstraint("amount > 0", name="check_positive_amount"),
        Index("ix_claim_car_date", "car_id", "claim_date"),
)