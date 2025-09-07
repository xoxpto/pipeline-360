from __future__ import annotations

import os
from pathlib import Path
from pydantic import BaseModel


class Settings(BaseModel):
    DATA_DIR: Path = Path("data")
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Path = Path("logs/pipeline.log")


def _strip_quotes(s: str | os.PathLike | None) -> str | None:
    if s is None:
        return None
    s = str(s)
    if len(s) >= 2 and s[0] == s[-1] and s[0] in {"'", '"'}:
        return s[1:-1]
    return s


def _load_envfile(path: Path) -> dict[str, str]:
    """Carrega um ficheiro .env simples (KEY=VALUE), ignorando comentários e linhas vazias."""
    out: dict[str, str] = {}
    try:
        if not path or not path.is_file():
            return out
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            out[k.strip()] = _strip_quotes(v.strip()) or ""
    except Exception:
        # silencioso: sem bloquear se não conseguir ler
        return {}
    return out


def get_settings() -> Settings:
    """
    Precedência:
      1) Variáveis de ambiente (inclui overrides via CLI/temp_env/pytest)
      2) Ficheiro apontado por PIPELINE360_ENV (se existir)
      3) Defaults
    """
    envfile = os.environ.get("PIPELINE360_ENV")
    from_file = _load_envfile(Path(envfile)) if envfile else {}

    def pick(key: str, default: str) -> str:
        v_env = os.environ.get(key)
        if v_env is not None and v_env != "":
            return _strip_quotes(v_env)  # ENV vence
        if key in from_file and from_file[key] not in (None, ""):
            return from_file[key]  # depois .env
        return default  # fallback

    data_dir = Path(pick("DATA_DIR", "data"))
    log_level = pick("LOG_LEVEL", "INFO")
    log_file = Path(pick("LOG_FILE", "logs/pipeline.log"))
    return Settings(DATA_DIR=data_dir, LOG_LEVEL=log_level, LOG_FILE=log_file)
