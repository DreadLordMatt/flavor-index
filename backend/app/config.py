from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    database_url: str = Field(
        default_factory=lambda: f"sqlite:///{(Path(__file__).resolve().parents[2] / 'flavor_index.db').as_posix()}"
    )
    environment: str = Field(default="development")

    class Config:
        env_prefix = "FLAVOR_INDEX_"
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached Settings instance."""

    return Settings()
