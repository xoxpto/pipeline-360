import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from .config import LOG_LEVEL as CFG_LEVEL, LOG_FILE as CFG_FILE

_configured = False

def setup_logging(level: str | None = None, log_file: Path | None = None):
    """
    (Re)configura o root logger com consola + ficheiro rotativo.
    Pode ser chamado várias vezes (limpa handlers).
    """
    global _configured
    lvl = getattr(logging, (level or CFG_LEVEL).upper(), logging.INFO)
    file = Path(log_file or CFG_FILE)

    root = logging.getLogger()
    # limpar handlers antigos
    for h in list(root.handlers):
        root.removeHandler(h)
        try:
            h.close()
        except Exception:
            pass

    root.setLevel(lvl)
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    root.addHandler(ch)

    file.parent.mkdir(parents=True, exist_ok=True)
    fh = RotatingFileHandler(file, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    fh.setFormatter(fmt)
    root.addHandler(fh)

    _configured = True

def get_logger(name: str) -> logging.Logger:
    # garante pelo menos configuração default
    if not _configured:
        setup_logging()
    return logging.getLogger(name)
