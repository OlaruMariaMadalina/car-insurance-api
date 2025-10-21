from sqlalchemy import String, Integer, Date, DECIMAL, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.car import Car
from app.models.policy import InsurancePolicy

class Claim(Base):
    __tablename__ = "claims"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    claim_date: Mapped[Date] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(DECIMAL(12, 2), nullable=False)

    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id", ondelete="CASCADE"))
    car: Mapped["Car"] = relationship("Car", back_populates="claims")

    policy_id: Mapped[int] = mapped_column(ForeignKey("insurance_policies.id", ondelete="RESTRICT"), nullable=False)
    policy: Mapped["InsurancePolicy"] = relationship("InsurancePolicy")

    __table_args__ = (
        CheckConstraint("amount > 0", name="check_positive_amount"),
        Index("ix_claim_car_date", "car_id", "claim_date"),
        Index("ix_claim_policy", "policy_id"),
)