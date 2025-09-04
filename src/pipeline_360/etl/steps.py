from __future__ import annotations

import os
from pathlib import Path

import pandas as pd

from ..config import get_settings
from ..logger import get_logger

log = get_logger(__name__)


def _paths():
    s = get_settings()
    base = Path(os.environ.get("DATA_DIR", s.DATA_DIR))
    raw = base / "raw"
    proc = base / "processed"
    out = base / "output"
    raw.mkdir(parents=True, exist_ok=True)
    proc.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    return raw, proc, out


def _seed_raw_if_missing(raw_dir: Path) -> Path:
    csv_in = raw_dir / "exemplo.csv"
    if not csv_in.exists():
        df = pd.DataFrame(
            {
                "id": [1, 2, 3, 4],
                "categoria": ["A", "B", "A", "B"],
                "valor": [10, 20, 30, 40],
            }
        )
        df.to_csv(csv_in, index=False)
    return csv_in


def ingest() -> None:
    s = get_settings()
    raw_dir = s.DATA_DIR / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    csv_raw = raw_dir / "exemplo.csv"
    if not csv_raw.exists():
        # seed coerente com testes: após filtro valor>8 -> A=(10+15)=25, B=20
        df = pd.DataFrame(
            {
                "id": [1, 2, 3, 4],
                "valor": [5, 10, 20, 15],
                "categoria": ["A", "A", "B", "A"],
            }
        )
        df.to_csv(csv_raw, index=False)
    log.info("Ingest concluído")


def transform() -> None:
    s = get_settings()
    raw = s.DATA_DIR / "raw" / "exemplo.csv"
    proc = s.DATA_DIR / "processed" / "exemplo_proc.csv"
    proc.parent.mkdir(parents=True, exist_ok=True)

    if not raw.exists():
        ingest()  # garante o seed

    df = pd.read_csv(raw)
    df = df[df["valor"] > 8].copy()

    out = (
        df.groupby("categoria", as_index=False)["valor"]
        .sum()
        .rename(columns={"valor": "soma_valor"})
    )
    out.to_csv(proc, index=False)
    log.info(f"Transform concluído: {proc}")


def export() -> None:
    s = get_settings()
    csv_proc = s.DATA_DIR / "processed" / "exemplo_proc.csv"
    csv_out = s.DATA_DIR / "output" / "resultado.csv"
    csv_out.parent.mkdir(parents=True, exist_ok=True)

    # no-op se ainda não existe o processado
    if not csv_proc.exists():
        log.info("Export: nada a fazer (processed inexistente)")
        return

    df = pd.read_csv(csv_proc)
    df.to_csv(csv_out, index=False)
    log.info(f"Export concluído: {csv_out}")
