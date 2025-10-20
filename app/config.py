from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "car-insurance-api"
    app_env: str = "dev"                  # dev/prod/test
    log_level: str = "INFO"
    database_url: str = "sqlite+aiosqlite:///./dev.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()