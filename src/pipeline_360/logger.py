import logging
from pathlib import Path
import sys


def setup_logging(level: str = "INFO", log_file: Path | str | None = None):
    lvl = getattr(logging, str(level).upper(), logging.INFO)

    # Limpa handlers antigos (evita lock de ficheiro no Windows)
    root = logging.getLogger()
    for h in list(root.handlers):
        try:
            h.close()
        except Exception:
            pass
        root.removeHandler(h)

    handlers: list[logging.Handler] = [
        logging.StreamHandler()
    ]  # caplog ainda vai anexar o dele

    if log_file:
        try:
            lf = Path(str(log_file))
            lf.parent.mkdir(parents=True, exist_ok=True)
            file_h = logging.FileHandler(lf, encoding="utf-8")
            handlers.append(file_h)
        except Exception as e:
            # Falhou ficheiro? mantém só consola e segue.
            print(
                f"[logger] aviso: não consegui abrir LOG_FILE ({e}); a registar só na consola.",
                file=sys.stdout,
            )

    logging.basicConfig(
        level=lvl,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=handlers,
    )


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    # Garante que herda do root (caplog capta) e propaga
    logger.setLevel(logging.NOTSET)
    logger.propagate = True
    return logger
