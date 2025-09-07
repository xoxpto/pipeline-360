from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

try:
    from rich.logging import RichHandler
except Exception:  # pragma: no cover - fallback sem rich
    RichHandler = None  # type: ignore


def _ensure_parent(path: Path) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass


def setup_logging(level: str = "INFO", log_file: str | Path = "logs/pipeline.log") -> None:
    """
    Configura logging:
      - Consola com Rich (se disponível)
      - Ficheiro (append) se o caminho for válido; senão, continua só consola
    Ao reconfigurar, remove handlers de ficheiro anteriores e mantém apenas um handler de consola.
    """
    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Remover FileHandlers antigos (evita leaks e falhas a apagar ficheiros)
    for h in list(root.handlers):
        if isinstance(h, logging.FileHandler):
            try:
                h.close()
            finally:
                root.removeHandler(h)

    # Garantir um único handler de consola
    has_console = any(
        (isinstance(h, RichHandler) if RichHandler else isinstance(h, logging.StreamHandler))
        for h in root.handlers
    )
    if not has_console:
        if RichHandler:
            ch = RichHandler(rich_tracebacks=False, show_time=True, show_level=True, show_path=False)
        else:  # pragma: no cover
            ch = logging.StreamHandler()
        ch.setLevel(getattr(logging, level.upper(), logging.INFO))
        ch.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
        root.addHandler(ch)

    # Tentar ficheiro
    try:
        lf = Path(log_file)
        _ensure_parent(lf)
        fh = logging.FileHandler(lf, mode="a", encoding="utf-8")
        fh.setLevel(getattr(logging, level.upper(), logging.INFO))
        fh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
        root.addHandler(fh)
    except Exception as e:  # falha → consola apenas
        print(f"[logger] aviso: não consegui abrir LOG_FILE ({e}); a registar só na consola.")


def get_logger(name: Optional[str] = None) -> logging.Logger:
    return logging.getLogger(name if name else "")
