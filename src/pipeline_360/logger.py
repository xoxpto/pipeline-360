import logging
from logging.handlers import RotatingFileHandler
from .config import LOG_LEVEL, LOG_FILE

_configured = False  # garante configuração única por processo

def _ensure_root_handlers():
    global _configured
    if _configured:
        return
    level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    logging.getLogger().setLevel(level)

    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    # Consola (apenas se não existir já)
    if not any(isinstance(h, logging.StreamHandler) for h in logging.getLogger().handlers):
        ch = logging.StreamHandler()
        ch.setFormatter(fmt)
        logging.getLogger().addHandler(ch)

    # Ficheiro rotativo (garantir sempre)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not any(isinstance(h, RotatingFileHandler) for h in logging.getLogger().handlers):
        fh = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
        fh.setFormatter(fmt)
        logging.getLogger().addHandler(fh)

    _configured = True

def get_logger(name: str) -> logging.Logger:
    _ensure_root_handlers()
    # usar logger de módulo; as mensagens propagam para o root (file + console)
    logger = logging.getLogger(name)
    logger.propagate = True
    return logger
