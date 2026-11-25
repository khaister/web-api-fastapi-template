from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    App settings, read from environment variables (and an optional, git-ignored `.env` file).

    Use `ENVIRONMENT` to tell deployments apart (`local`, `staging`, `prod`); everything else is
    overridden per environment through the variables below, e.g. `DATABASE_URL`.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "local"
    log_level: str = "INFO"

    # clients send this in the `X-API-Key` header; when unset, every authenticated request is rejected
    api_key: str | None = None

    database_url: str = "sqlite+aiosqlite:///./app.db"

    sample_api_base_url: str = "https://api.sampleapis.com"

    @property
    def is_local(self) -> bool:
        return self.environment == "local"


@lru_cache
def get_settings() -> Settings:
    return Settings()
