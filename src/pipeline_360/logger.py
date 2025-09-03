from __future__ import annotations

import logging
from logging import Handler
from pathlib import Path
from typing import Optional


def setup_logging(level: str = "INFO", log_file: Optional[Path] = None) -> None:
    """
    Configura logging no *root*:
      - Sempre consola (StreamHandler)
      - Tentar ficheiro, mas se falhar, não rebenta (imprime aviso e segue só com consola)
    Isto garante que caplog (pytest) apanha as mensagens.
    """
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))

    # consola
    sh = logging.StreamHandler()
    sh.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    )
    root.addHandler(sh)

    # ficheiro (opcional)
    if log_file:
        try:
            Path(log_file).parent.mkdir(parents=True, exist_ok=True)
            fh: Handler = logging.FileHandler(log_file, encoding="utf-8")
            fh.setFormatter(
                logging.Formatter(
                    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
                )
            )
            root.addHandler(fh)
        except Exception as e:
            print(
                f"[logger] aviso: não consegui abrir LOG_FILE ({e}); a registar só na consola."
            )

    # Não adicionar handlers em loggers filhos; deixar propagar
    # (por omissão propagate=True -> caplog apanha)
    # Nada a fazer aqui, apenas não configurar handlers específicos por logger.


def get_logger(name: str) -> logging.Logger:
    # herda dos handlers do root (configurados em setup_logging)
    return logging.getLogger(name)
