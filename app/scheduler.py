from __future__ import annotations
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import timedelta
from app.jobs.policy_expiry import run_policy_expiry_scan
import structlog
from app.config import settings

log = structlog.get_logger()

class Scheduler:
    def __init__(self, interval_minutes: int = 10, timezone: str = "Europe/Bucharest"):
        self.scheduler = AsyncIOScheduler(timezone=timezone)
        self.interval_minutes = interval_minutes
        
    def start(self):
        self.scheduler.add_job(
            run_policy_expiry_scan,
            "interval",
            minutes=self.interval_minutes,
            id="policy_expiry_scan",
            coalesce=True,
            max_instances=1,
            misfire_grace_time=60,
        )
        self.scheduler.start()
        log.info("scheduler_started", interval_minutes=self.interval_minutes)
        
    def shutdown(self):
        self.scheduler.shutdown(wait=False)
        log.info("scheduler_stopped")
        
scheduler_singleton = Scheduler(interval_minutes=settings.expiry_scan_interval_minutes)    
    