from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    DATA_DIR: Path = Field(default=Path("data"))
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FILE: Path = Field(default=Path("logs") / "pipeline.log")

settings = Settings()
DATA_DIR: Path = settings.DATA_DIR
LOG_LEVEL: str = settings.LOG_LEVEL
LOG_FILE: Path = settings.LOG_FILE

__all__ = ["settings", "DATA_DIR", "LOG_LEVEL", "LOG_FILE"]
