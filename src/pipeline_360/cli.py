import typer
from rich import print
from .logger import get_logger

app = typer.Typer(help="CLI do Pipeline 360")
log = get_logger(__name__)

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

def main():
    app()