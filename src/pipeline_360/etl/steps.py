from __future__ import annotations

from pathlib import Path

import pandas as pd

from ..config import get_settings
from ..logger import get_logger

log = get_logger("pipeline_360.etl.steps")


def _ensure_dirs(base: Path) -> None:
    for d in (base / "raw", base / "processed", base / "output"):
        d.mkdir(parents=True, exist_ok=True)


def ingest() -> Path:
    """Gera (se não existir) raw/exemplo.csv com dados de seed."""
    s = get_settings()
    _ensure_dirs(s.DATA_DIR)

    raw_csv = s.DATA_DIR / "raw" / "exemplo.csv"
    if not raw_csv.exists():
        df = pd.DataFrame(
            [
                {"id": 1, "categoria": "A", "valor": 5},
                {"id": 2, "categoria": "A", "valor": 10},
                {"id": 3, "categoria": "A", "valor": 15},
                {"id": 4, "categoria": "B", "valor": 7},
                {"id": 5, "categoria": "B", "valor": 20},
                {"id": 6, "categoria": "C", "valor": 3},
            ]
        )
        df.to_csv(raw_csv, index=False)
    log.info("Ingest concluído")
    return raw_csv


def transform() -> Path:
    """Lê raw/exemplo.csv, filtra valor>8, agrupa por categoria e soma apenas 'valor'."""
    s = get_settings()
    _ensure_dirs(s.DATA_DIR)

    raw_csv = s.DATA_DIR / "raw" / "exemplo.csv"
    if not raw_csv.exists():
        ingest()  # garante seed

    df = pd.read_csv(raw_csv)
    df = df[df["valor"] > 8]
    out = (
        df.groupby("categoria", as_index=False)["valor"]
        .sum()
        .rename(columns={"valor": "soma_valor"})
    )

    proc_csv = s.DATA_DIR / "processed" / "exemplo_proc.csv"
    out.to_csv(proc_csv, index=False)
    log.info(f"Transform concluído: {proc_csv}")
    return proc_csv


def export() -> Path | None:
    """Copia processed para output/resultado.csv. Se não existir processed, é no-op com log."""
    s = get_settings()
    _ensure_dirs(s.DATA_DIR)
    proc_csv = s.DATA_DIR / "processed" / "exemplo_proc.csv"
    if not proc_csv.exists():
        log.info("Export: nada a fazer (processed inexistente)")
        return None
    df = pd.read_csv(proc_csv)
    out_csv = s.DATA_DIR / "output" / "resultado.csv"
    df.to_csv(out_csv, index=False)
    log.info(f"Export concluído: {out_csv}")
    return out_csv
