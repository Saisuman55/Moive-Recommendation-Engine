from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Always resolve `backend/.env` (not cwd) so uvicorn/pytest work from repo root or `backend/`.
_BACKEND_DIR = Path(__file__).resolve().parent.parent
_ENV_PATH = _BACKEND_DIR / ".env"
_SETTINGS_ENV = (
    {"env_file": str(_ENV_PATH), "env_file_encoding": "utf-8"} if _ENV_PATH.is_file() else {}
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(**_SETTINGS_ENV, extra="ignore")

    # Default to SQLite so `uvicorn` works without Docker/Postgres. Docker Compose sets DATABASE_URL to Postgres.
    database_url: str = "sqlite:///./movie_rec.db"
    better_auth_url: str = "http://localhost:5173"
    better_auth_secret: str = "change-me-in-production-use-long-random-string"
    access_token_expire_minutes: int = 60 * 24 * 7
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    model_path: str = "./data/svd_model.pkl"
    debug: bool = Field(default=False, validation_alias="DEBUG")

    @property
    def jwt_secret(self) -> str:
        return self.better_auth_secret

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
