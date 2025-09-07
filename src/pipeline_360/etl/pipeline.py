from __future__ import annotations

from ..logger import get_logger
from .steps import ingest, transform, export

log = get_logger("pipeline_360.etl.pipeline")


def run_pipeline(stage: str = "all") -> None:
    log.info("Ingest iniciado")
    if stage in {"ingest", "all"}:
        ingest()
        log.info("Ingest concluído")

    if stage in {"transform", "all"}:
        log.info("Transform iniciado")
        transform()
        log.info("Transform concluído")

    if stage in {"export", "all"}:
        log.info("Export iniciado")
        export()
        log.info("Export concluído")
