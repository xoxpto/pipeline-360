from pathlib import Path
import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
    DATA_DIR: Path = Field(default=Path("data"))
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FILE: Path = Field(default=Path("logs") / "pipeline.log")


def _strip_quotes(p: Path | str) -> Path:
    s = str(p).strip().strip('"').strip("'")
    return Path(s)


def get_settings() -> Settings:
    # Se existir um .env alternativo via variável, usa-o. Caso contrário usa .env padrão.
    env_path = os.environ.get("PIPELINE360_ENV")
    s = Settings(_env_file=env_path) if env_path else Settings()
    # Normaliza caminhos caso venham entre aspas
    return s.model_copy(
        update={
            "DATA_DIR": _strip_quotes(s.DATA_DIR),
            "LOG_FILE": _strip_quotes(s.LOG_FILE),
        }
    )


# Expor defaults de módulo (vários componentes importam estes)
settings = get_settings()
DATA_DIR: Path = settings.DATA_DIR
LOG_LEVEL: str = settings.LOG_LEVEL
LOG_FILE: Path = settings.LOG_FILE

__all__ = ["Settings", "get_settings", "settings", "DATA_DIR", "LOG_LEVEL", "LOG_FILE"]
