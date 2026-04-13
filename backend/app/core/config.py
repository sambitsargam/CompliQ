from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "CompliQ API"
    app_version: str = "0.1.0"
    database_url: str = "sqlite:///./compliq.db"
    cors_origins: str = "http://localhost:3000"

    openai_api_key: str | None = None
    use_neuro_san: bool = True

    upload_dir: str = "./storage/uploads"
    reports_dir: str = "./storage/reports"


@lru_cache
def get_settings() -> Settings:
    return Settings()
