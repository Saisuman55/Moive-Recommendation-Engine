from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Default to SQLite so `uvicorn` works without Docker/Postgres. Docker Compose sets DATABASE_URL to Postgres.
    database_url: str = "sqlite:///./movie_rec.db"
    better_auth_url: str = "http://localhost:5173"
    better_auth_secret: str = "change-me-in-production-use-long-random-string"
    access_token_expire_minutes: int = 60 * 24 * 7
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    model_path: str = "./data/svd_model.pkl"

    @property
    def jwt_secret(self) -> str:
        return self.better_auth_secret

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
