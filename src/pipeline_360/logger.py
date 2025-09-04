from __future__ import annotations

import logging
from pathlib import Path
from rich.logging import RichHandler


def _has_handler(logger: logging.Logger, handler_type: type) -> bool:
    return any(isinstance(h, handler_type) for h in logger.handlers)


def setup_logging(
    level: str = "INFO", log_file: str | Path | None = "logs/pipeline.log"
) -> None:
    """
    Configura logging com Rich na consola e (opcionalmente) ficheiro.
    - Se log_file for None, não cria FileHandler (consola apenas).
    - Remove e fecha FileHandlers antigos para evitar handlers “pendurados” entre testes.
    - Valida caminho do ficheiro; em erro faz fallback para consola.
    """
    root = logging.getLogger()
    root.setLevel(level)

    # consola: garantir um único RichHandler
    if not _has_handler(root, RichHandler):
        console = RichHandler(rich_tracebacks=False, markup=True)
        console.setLevel(level)
        console.setFormatter(logging.Formatter("%(message)s"))
        root.addHandler(console)

    # limpar file handlers antigos
    old_file_handlers = [h for h in root.handlers if isinstance(h, logging.FileHandler)]
    for h in old_file_handlers:
        try:
            h.close()
        finally:
            root.removeHandler(h)

    # sem ficheiro? consola only
    if not log_file:
        return

    # tentar adicionar file handler de forma segura
    try:
        lp = Path(log_file)
        lp.parent.mkdir(parents=True, exist_ok=True)

        # valida (abre/fecha) – se falhar, não adiciona
        try:
            with lp.open("a", encoding="utf-8"):
                pass
        except Exception as e:
            print(
                f"[logger] aviso: não consegui abrir LOG_FILE ({e}); a registar só na consola."
            )
            return

        fh = logging.FileHandler(lp, mode="a", encoding="utf-8", delay=True)
        fh.setLevel(level)
        fh.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        )
        root.addHandler(fh)

    except Exception as e:
        print(
            f"[logger] aviso: não consegui abrir LOG_FILE ({e}); a registar só na consola."
        )


def get_logger(name: str | None = None) -> logging.Logger:
    return logging.getLogger(name if name else "")
