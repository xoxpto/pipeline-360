from __future__ import annotations

import os
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Settings:
    DATA_DIR: Path = Path("data")
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Path = Path("logs/pipeline.log")


def _parse_line(line: str) -> tuple[str, str] | None:
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
        return None
    k, v = line.split("=", 1)
    k = k.strip()
    v = v.strip().strip('"').strip("'")  # tirar aspas se existirem
    return k, v


def _load_envfile(path: Path) -> dict[str, str]:
    """
    Lê um .env simples. Se `path` não existir ou não for ficheiro, devolve {}.
    Nunca tenta ler diretórios (evita PermissionError em Path('.')).
    """
    if not path or not isinstance(path, Path) or not path.is_file():
        return {}

    out: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        kv = _parse_line(line)
        if kv:
            k, v = kv
            out[k] = v
    return out


def get_settings() -> Settings:
    """
    Recolhe as definições por esta ordem:
    1) PIPELINE360_ENV -> caminho para .env (opcional)
    2) Variáveis de ambiente (DATA_DIR, LOG_FILE, LOG_LEVEL)
    3) Defaults
    """
    # 1) carregar de ficheiro, se indicado
    envfile = os.environ.get("PIPELINE360_ENV")
    from_file = _load_envfile(Path(envfile)) if envfile else {}

    # 2) sobrepor com variáveis de ambiente diretas, se existirem
    data_dir = os.environ.get("DATA_DIR", from_file.get("DATA_DIR", "data"))
    log_level = os.environ.get("LOG_LEVEL", from_file.get("LOG_LEVEL", "INFO"))
    log_file = os.environ.get(
        "LOG_FILE", from_file.get("LOG_FILE", "logs/pipeline.log")
    )

    # normalizar Paths
    return Settings(
        DATA_DIR=Path(data_dir), LOG_LEVEL=log_level, LOG_FILE=Path(log_file)
    )
