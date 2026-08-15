# pydantic-settings, env var support
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "book-analytics-api"
    ENV: str = "local"

    # SQLite DB path — swapped for PostgreSQL/MySQL in production via env var
    DATABASE_URL: str = "sqlite:///./book_analytics.db"

    # Auth — simple API key (demonstrates security pattern without Keycloak dependency)
    API_KEY: str = "dev-api-key-change-in-production"

    # CORS
    CORS_ORIGINS: list[str] = ["*"]


settings = Settings()