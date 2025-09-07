from __future__ import annotations

import logging
import os
import shutil
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, Iterator, Optional

import typer

from .config import get_settings
from .etl.pipeline import run_pipeline
from .logger import get_logger, setup_logging

app = typer.Typer(help="CLI do Pipeline 360")


@contextmanager
def temp_env(overrides: Dict[str, str]) -> Iterator[None]:
    """Define variáveis de ambiente temporariamente (para precedence em get_settings)."""
    old: Dict[str, Optional[str]] = {}
    try:
        for k, v in overrides.items():
            old[k] = os.environ.get(k)
            os.environ[k] = str(v)
        yield
    finally:
        for k, v in old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


@contextmanager
def masked_env(unset_keys: list[str]) -> Iterator[None]:
    """
    Remove temporariamente certas variáveis de ambiente.
    Útil para garantir que --config (dotenv) vence ENV preexistente.
    """
    saved: dict[str, Optional[str]] = {}
    try:
        for k in unset_keys:
            saved[k] = os.environ.get(k)
            if k in os.environ:
                del os.environ[k]
        yield
    finally:
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


@app.callback()
def main(
    ctx: typer.Context,
    config: Optional[Path] = typer.Option(
        None, "--config", help="Ficheiro .env alternativo"
    ),
    data_dir: Optional[Path] = typer.Option(
        None, "--data-dir", help="Override do DATA_DIR"
    ),
    log_level: Optional[str] = typer.Option(
        None, "--log-level", help="Override do LOG_LEVEL"
    ),
    log_file: Optional[Path] = typer.Option(
        None, "--log-file", help="Override do LOG_FILE"
    ),
):
    # Se veio --config, define já para get_settings() ver
    has_config = config is not None
    if has_config:
        os.environ["PIPELINE360_ENV"] = str(config)

    # Flags explícitas que queremos forçar (vencem tudo)
    overrides = {
        **({"DATA_DIR": str(data_dir)} if data_dir else {}),
        **({"LOG_LEVEL": str(log_level)} if log_level else {}),
        **({"LOG_FILE": str(log_file)} if log_file else {}),
    }

    # Se há --config mas NÃO há overrides para estes 3, vamos
    # mascarar as ENV para que o dotenv seja aplicado de facto.
    to_mask: list[str] = []
    if has_config:
        for k in ("DATA_DIR", "LOG_LEVEL", "LOG_FILE"):
            if k not in overrides:
                to_mask.append(k)

    ctx.obj = {"overrides": overrides, "mask_keys": to_mask}


@app.command()
def hello(name: str = typer.Option("mundo", "--name", "-n")):
    """Só um olá para testar a CLI."""
    setup_logging()
    log = get_logger("pipeline_360.cli")
    log.info("hello chamado")
    typer.echo(f"Olá, {name}!")


@app.command()
def run(
    stage: str = typer.Option(
        "all",
        "--stage",
        "-s",
        case_sensitive=False,
        help="Etapa a executar: ingest | transform | export | all",
    ),
    ctx: typer.Context = typer.Option(None),
):
    """Executa a pipeline."""
    ov = (ctx.obj or {}).get("overrides", {})
    mask_keys: list[str] = (ctx.obj or {}).get("mask_keys", [])
    with masked_env(mask_keys):
        with temp_env(ov):
            s = get_settings()
            setup_logging(level=s.LOG_LEVEL, log_file=s.LOG_FILE)
            log = get_logger("pipeline_360.cli")
            log.info(f"Run stage={stage.lower()}")
            run_pipeline(stage.lower())


@app.command()
def clean(
    yes: bool = typer.Option(False, "--yes", "-y", help="Não pedir confirmação"),
    ctx: typer.Context = typer.Option(None),
):
    """Remove raw/processed/output e o log_file configurado."""
    ov = (ctx.obj or {}).get("overrides", {})
    mask_keys: list[str] = (ctx.obj or {}).get("mask_keys", [])

    with masked_env(mask_keys):
        with temp_env(ov):
            s = get_settings()
            setup_logging(level=s.LOG_LEVEL, log_file=s.LOG_FILE)
            log = get_logger("pipeline_360.cli")

            base = s.DATA_DIR
            targets = [base / "raw", base / "processed", base / "output"]

            if not yes:
                typer.confirm(
                    f"Apagar {', '.join(str(t) for t in targets)} e o log '{s.LOG_FILE}'?",
                    abort=True,
                )

            # Remover handlers de ficheiro antes de apagar logs/diretórios,
            # e manter apenas a consola activa
            root = logging.getLogger()
            for h in list(root.handlers):
                if isinstance(h, logging.FileHandler):
                    try:
                        h.close()
                    finally:
                        root.removeHandler(h)

            # Apagar subpastas de dados
            for t in targets:
                try:
                    shutil.rmtree(t, ignore_errors=True)
                except Exception as e:
                    log.warning(f"Falha a apagar {t}: {e}")

            # Apagar diretório base (se existir)
            try:
                shutil.rmtree(base, ignore_errors=True)
            except Exception as e:
                log.warning(f"Falha a apagar {base}: {e}")

            # Apagar log_file (fora do DATA_DIR)
            try:
                lf = Path(s.LOG_FILE)
                if lf.exists():
                    lf.unlink(missing_ok=True)
                # tentar remover pasta de logs se ficar vazia
                if lf.parent.exists():
                    try:
                        lf.parent.rmdir()
                    except Exception:
                        pass
            except Exception as e:
                log.warning(f"Falha a apagar log_file {s.LOG_FILE}: {e}")

            log.info("Clean concluído")
