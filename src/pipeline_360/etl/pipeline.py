from .steps import ingest, transform, export
from ..logger import get_logger

log = get_logger(__name__)

def run_pipeline(stage: str = "all") -> None:
    if stage in ("ingest", "all"):
        log.info("Ingest iniciado")
        ingest()
        log.info("Ingest concluído")

    if stage in ("transform", "all"):
        log.info("Transform iniciado")
        transform()
        log.info("Transform concluído")

    if stage in ("export", "all"):
        log.info("Export iniciado")
        export()
        log.info("Export concluído")
