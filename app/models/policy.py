from sqlalchemy import String, Integer, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.car import Car

class InsurancePolicy(Base):
    __tablename__="insurance_policies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    provider: Mapped[str] = mapped_column(String(100), nullable=False)
    policy_number: Mapped[str] = mapped_column(String(64), nullable=False)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)

    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id", ondelete="CASCADE"))
    car: Mapped["Car"] = relationship("Car", back_populates="policies")

    __table_args__ = (CheckConstraint("end_date >= start_date", name="check_valid_policy_dates"),)