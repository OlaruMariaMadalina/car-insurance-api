from pydantic_settings import BaseSettings, SettingsConfigDict
from zoneinfo import ZoneInfo
from pydantic import Field
from typing import ClassVar

class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables or defaults.

    Attributes:
        app_name (str): The name of the application.
        app_env (str): The environment (e.g., 'dev', 'prod').
        log_level (str): Logging level for the application.
        database_url (str): Database connection URL.
        LOCAL_TZ (ZoneInfo): Local timezone for the application.
        expiry_scan_interval_minutes (int): Interval in minutes for policy expiry scan jobs.
        model_config (SettingsConfigDict): Pydantic settings for environment file loading.
    """
    app_name: str = "car-insurance-api"
    app_env: str = "dev"                  
    log_level: str = "INFO"
    database_url: str = "sqlite+aiosqlite:///./dev.db"
    LOCAL_TZ: ClassVar[ZoneInfo] = ZoneInfo("Europe/Bucharest")
    expiry_scan_interval_minutes: int = Field(default=10, alias="EXPIRY_SCAN_INTERVAL_MINUTES")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()