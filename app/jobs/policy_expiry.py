from __future__ import annotations
from datetime import datetime, time, timedelta
import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.engine import SessionLocal
from app.models.policy import InsurancePolicy
from app.config import settings

log = structlog.get_logger()

async def _scan_and_log_today_expiries(session: AsyncSession, now: datetime) -> None:
    today = now.date()
    
    statement = (
        select(InsurancePolicy)
        .where(
            InsurancePolicy.end_date <= today,
            InsurancePolicy.logged_expiry_at.is_(None),    
        )
    )
    
    result = await session.execute(statement)
    
    policies = result.scalars().all()
    
    if not policies:
        return
    
    for p in policies:
        log.info(
            "policy_expired",
            policy_id=p.id,
            car_id=p.car_id,
            end_date=p.end_date.isoformat(),
            message=f"Policy {p.id} for car {p.car_id} expired on {p.end_date}",
        )
        p.logged_expiry_at = now
        
    await session.commit()
    
def _in_first_hour_of_today(now: datetime) -> bool:
    today_start = datetime.combine(now.date(), time(0,0), tzinfo=now.tzinfo)
    # return today_start <= now < (today_start + timedelta(hours=1))
    return True

async def run_policy_expiry_scan() -> None:
    
    now = datetime.now(settings.LOCAL_TZ)
    
    if not _in_first_hour_of_today(now): 
        return
    
    async with SessionLocal() as session:
        await _scan_and_log_today_expiries(session, now)
        
        