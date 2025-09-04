# topo do ficheiro
import os
from contextlib import contextmanager
from typing import Optional
from pathlib import Path
import typer
import logging
import shutil
from rich import print as rprint

from .config import get_settings
from .logger import setup_logging, get_logger
from .etl.pipeline import run_pipeline

app = typer.Typer(help="CLI do Pipeline 360")


@contextmanager
def temp_env(new: dict[str, str]):
    old = {}
    sentinel = object()
    try:
        for k, v in new.items():
            old[k] = os.environ.get(k, sentinel)
            os.environ[k] = v
        yield
    finally:
        for k, v in old.items():
            if v is sentinel:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


def _build_env_overrides(
    data_dir: Optional[Path],
    log_file: Optional[Path],
    log_level: Optional[str],
    config: Optional[Path],
) -> dict[str, str]:
    env: dict[str, str] = {}
    if config:
        env["PIPELINE360_ENV"] = str(config)
    if data_dir:
        env["DATA_DIR"] = str(data_dir)
    if log_file:
        env["LOG_FILE"] = str(log_file)
    if log_level:
        env["LOG_LEVEL"] = log_level
    return env


@app.callback()
def global_options(
    ctx: typer.Context,
    data_dir: Optional[Path] = typer.Option(None, help="Diretório base de dados"),
    log_file: Optional[Path] = typer.Option(None, help="Ficheiro de logs"),
    log_level: Optional[str] = typer.Option(
        None, help="Nivel de log (DEBUG, INFO, ...)"
    ),
    config: Optional[Path] = typer.Option(None, "--config", help="Caminho para .env"),
):
    """Não altera o ambiente global; apenas guarda overrides para este comando."""
    ctx.obj = {"overrides": _build_env_overrides(data_dir, log_file, log_level, config)}


@app.command()
def hello(
    name: str = typer.Option("mundo", "--name", "-n"),
    ctx: typer.Context = typer.Option(None),
):
    ov = (ctx.obj or {}).get("overrides", {})
    with temp_env(ov):
        s = get_settings()
        setup_logging(level=s.LOG_LEVEL, log_file=s.LOG_FILE)
        log = get_logger("pipeline_360.cli")
        log.info("hello chamado")
        rprint(f"Olá, {name}!")


@app.command()
def run(
    stage: str = typer.Option(
        "all", "--stage", help="ingest | transform | export | all"
    ),
    ctx: typer.Context = typer.Option(None),
):
    ov = (ctx.obj or {}).get("overrides", {})
    with temp_env(ov):
        s = get_settings()
        setup_logging(level=s.LOG_LEVEL, log_file=s.LOG_FILE)
        log = get_logger("pipeline_360.cli")
        log.info(f"Run stage={stage}")
        run_pipeline(stage)


@app.command()
def clean(
    yes: bool = typer.Option(False, "--yes", "-y", help="Não pedir confirmação"),
    ctx: typer.Context = typer.Option(None),
):
    """Remove raw/processed/output do DATA_DIR e apaga o ficheiro de log."""
    ov = (ctx.obj or {}).get("overrides", {})
    with temp_env(ov):
        s = get_settings()
        setup_logging(level=s.LOG_LEVEL, log_file=s.LOG_FILE)
        log = get_logger("pipeline_360.cli")

        base: Path = s.DATA_DIR
        targets = [base / "raw", base / "processed", base / "output"]

        if not yes:
            typer.confirm(f"Apagar {', '.join(str(t) for t in targets)} ?", abort=True)

        # 1) apagar subpastas e diretório base
        for t in targets:
            try:
                shutil.rmtree(t, ignore_errors=True)
            except Exception as e:
                log.warning(f"Falha a apagar {t}: {e}")

        try:
            shutil.rmtree(base, ignore_errors=True)
        except Exception as e:
            log.warning(f"Falha a apagar {base}: {e}")

        # 2) libertar handlers/locks do logging antes de apagar o ficheiro de log
        try:
            logging.shutdown()
            root = logging.getLogger()
            for h in root.handlers[:]:
                try:
                    h.flush()
                except Exception:
                    pass
                try:
                    h.close()
                except Exception:
                    pass
                root.removeHandler(h)
        except Exception:
            # sem logging aqui para não reabrir handlers
            pass

        # 3) apagar ficheiro de log e (se possível) a pasta onde está
        try:
            lf = Path(s.LOG_FILE) if s.LOG_FILE else None
            if lf and lf.exists():
                lf.unlink()
                # tenta remover diretório do log se estiver vazio
                try:
                    lf.parent.rmdir()
                except OSError:
                    pass
        except Exception:
            # sem logging aqui para evitar reacender handlers
            pass


@app.command()
def main() -> None:
    """Entry-point para `python -m pipeline_360`."""
    app()
