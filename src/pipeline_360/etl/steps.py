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


def ingest() -> Path:
    raw, _, _ = _paths()
    csv_in = _seed_raw_if_missing(raw)
    log.info("Ingest concluído")
    return csv_in


def transform() -> Path:
    raw, proc, _ = _paths()
    csv_in = _seed_raw_if_missing(raw)
    df = pd.read_csv(csv_in)
    # agrupamento pedido pelos testes
    out_df = (
        df.groupby("categoria", as_index=False)["valor"]
        .sum()
        .rename(columns={"valor": "soma_valor"})
    )
    csv_proc = proc / "exemplo_proc.csv"
    out_df.to_csv(csv_proc, index=False)
    log.info(f"Transform concluído: {csv_proc}")
    return csv_proc


def export() -> Path:
    _, _, out = _paths()
    csv_proc = out.parent / "processed" / "exemplo_proc.csv"
    if not csv_proc.exists():
        # garantir transform
        csv_proc = transform()
    df = pd.read_csv(csv_proc)
    csv_out = out / "resultado.csv"
    df.to_csv(csv_out, index=False)
    log.info(f"Export concluído: {csv_out}")
    return csv_out
