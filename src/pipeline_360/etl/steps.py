from pathlib import Path
from ..config import DATA_DIR

RAW = DATA_DIR / "raw"
PROC = DATA_DIR / "processed"
OUT = DATA_DIR / "output"

for d in (RAW, PROC, OUT):
    d.mkdir(parents=True, exist_ok=True)

def ingest():
    # TODO: substitui por ingestão real (APIs/CSV/etc.)
    (RAW / "exemplo.txt").write_text("dados brutos", encoding="utf-8")

def transform():
    # TODO: substitui por transform real (pandas, validação, etc.)
    src = RAW / "exemplo.txt"
    dst = PROC / "exemplo_proc.txt"
    if src.exists():
        dst.write_text(src.read_text(encoding="utf-8").upper(), encoding="utf-8")

def export():
    # TODO: substitui por export real (CSV final, DB, parquet, etc.)
    src = PROC / "exemplo_proc.txt"
    dst = OUT / "resultado.txt"
    if src.exists():
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
