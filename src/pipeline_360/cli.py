import os
import shutil
from pathlib import Path
import typer
from rich import print
from .logger import get_logger, setup_logging
from .config import Settings

app = typer.Typer(help="CLI do Pipeline 360")
log = get_logger(__name__)

@app.callback()
def main_options(
    data_dir: Path = typer.Option(None, "--data-dir", help="Diretório base de dados"),
    log_level: str = typer.Option(None, "--log-level", help="Nível de log (DEBUG/INFO/WARN/ERROR)"),
    log_file: Path = typer.Option(None, "--log-file", help="Ficheiro de log"),
):
    """
    Opções globais. Se fornecidas, sobrepõem .env via variáveis de ambiente.
    """
    if data_dir is not None:
        os.environ["DATA_DIR"] = str(data_dir)
    if log_level is not None:
        os.environ["LOG_LEVEL"] = str(log_level)
    if log_file is not None:
        os.environ["LOG_FILE"] = str(log_file)
    # reconfigurar logger com o que ficou no ambiente
    s = Settings()
    setup_logging(level=s.LOG_LEVEL, log_file=s.LOG_FILE)

@app.command()
def hello(name: str = "mundo"):
    """Comando de teste."""
    print(f"[bold green]Olá[/], {name}!")
    log.info("hello chamado")

@app.command()
def run(stage: str = typer.Option("all", help="Etapa a executar: ingest|transform|export|all")):
    """Executa o pipeline por etapas."""
    from .etl.pipeline import run_pipeline
    run_pipeline(stage)
    print("[bold green]Pipeline concluído[/]")

@app.command()
def clean(confirm: bool = typer.Option(True, "--yes/--no", help="Confirmar limpeza")):
    """Apaga conteúdo de data/ e logs/ (conforme config)."""
    s = Settings()
    if not confirm:
        print("[yellow]Operação cancelada[/]")
        raise typer.Exit(1)
    for p in [s.DATA_DIR, Path(s.LOG_FILE).parent]:
        if p.exists():
            shutil.rmtree(p)
            print(f"[cyan]Removido:[/] {p}")
    print("[bold green]Limpeza concluída[/]")
