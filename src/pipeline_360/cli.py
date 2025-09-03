import os
import time
import shutil
import typer
from pathlib import Path
from rich import print

from .config import get_settings
from .logger import get_logger, setup_logging

app = typer.Typer(help="CLI do Pipeline 360")
log = get_logger(__name__)


@app.callback()
def main_options(
    data_dir: Path = typer.Option(None, "--data-dir", help="Diretório base de dados"),
    log_level: str = typer.Option(
        None, "--log-level", help="Nível de log (DEBUG/INFO/WARN/ERROR)"
    ),
    log_file: Path = typer.Option(None, "--log-file", help="Ficheiro de log"),
    config: Path = typer.Option(
        None, "--config", help="Caminho para um .env alternativo"
    ),
):
    # --config: usar .env alternativo via variável
    if config is not None:
        for k in ("DATA_DIR", "LOG_LEVEL", "LOG_FILE"):
            os.environ.pop(k, None)
        os.environ["PIPELINE360_ENV"] = str(config)

    # Overrides diretos por flags
    if data_dir is not None:
        os.environ["DATA_DIR"] = str(data_dir)
    if log_level is not None:
        os.environ["LOG_LEVEL"] = str(log_level)
    if log_file is not None:
        os.environ["LOG_FILE"] = str(log_file)

    s = get_settings()
    setup_logging(level=s.LOG_LEVEL, log_file=s.LOG_FILE)


@app.command()
def hello(name: str = "mundo"):
    print(f"Olá, {name}!")
    log.info("hello chamado")


@app.command()
def run(
    stage: str = typer.Option(
        "all", help="Etapa a executar: ingest|transform|export|all"
    )
):
    from .etl.pipeline import run_pipeline

    run_pipeline(stage)
    print("Pipeline concluído")


@app.command()
def clean(yes: bool = typer.Option(False, "--yes", help="Não pedir confirmação")):
    s = get_settings()
    targets = [s.DATA_DIR, Path(s.LOG_FILE).parent]

    if not yes:
        typer.confirm(f"Confirma apagar {targets}?", abort=True)

    # libertar ficheiro de log se estiver aberto
    try:
        import logging

        logging.shutdown()
    except Exception:
        pass

    # tenta remover o ficheiro de log
    try:
        Path(s.LOG_FILE).unlink(missing_ok=True)
    except Exception:
        pass

    # remover diretórios com algumas tentativas; não falha em Windows
    for p in targets:
        if not p:
            continue
        for _ in range(5):
            try:
                if p.exists():
                    shutil.rmtree(p)
                    print(f"Removido: {p}")
                break
            except Exception:
                time.sleep(0.2)

    print("Clean concluído")


def main():
    app()
