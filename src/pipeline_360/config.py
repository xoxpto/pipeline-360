from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel


def _strip_quotes(s: str) -> str:
    s = s.strip()
    if (s.startswith('"') and s.endswith('"')) or (
        s.startswith("'") and s.endswith("'")
    ):
        return s[1:-1]
    return s


def _load_envfile(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if not path or not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = _strip_quotes(v.strip())
    return env


class Settings(BaseModel):
    DATA_DIR: Path = Path("data")
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Path = Path("logs/pipeline.log")


def get_settings(config: Optional[Path] = None) -> Settings:
    """
    Carrega settings na seguinte ordem (último ganha):
      1) defaults
      2) ficheiro .env indicado por 'config' OU por PIPELINE360_ENV (se existir)
      3) variáveis de ambiente atuais (DATA_DIR, LOG_LEVEL, LOG_FILE)
    """
    # 1) defaults
    values: dict[str, object] = {}

    # 2) envfile
    envfile = config or (
        Path(os.environ["PIPELINE360_ENV"]) if "PIPELINE360_ENV" in os.environ else None
    )
    from_file = _load_envfile(Path(envfile) if envfile else Path())
    values.update(from_file)

    # 3) overrides por ambiente
    for key in ("DATA_DIR", "LOG_LEVEL", "LOG_FILE"):
        if key in os.environ:
            values[key] = os.environ[key]

    # normalizar caminhos
    if "DATA_DIR" in values:
        values["DATA_DIR"] = Path(values["DATA_DIR"])
    if "LOG_FILE" in values:
        values["LOG_FILE"] = Path(values["LOG_FILE"])

    return Settings(**values)
