from pathlib import Path
import pandas as pd
from ..config import DATA_DIR

RAW = DATA_DIR / "raw"
PROC = DATA_DIR / "processed"
OUT = DATA_DIR / "output"

for d in (RAW, PROC, OUT):
    d.mkdir(parents=True, exist_ok=True)

CSV_IN = RAW / "exemplo.csv"
CSV_PROC = PROC / "exemplo_proc.csv"
CSV_OUT = OUT / "resultado.csv"

def _seed_example_csv():
    if not CSV_IN.exists():
        df = pd.DataFrame(
            {
                "id": [1, 2, 3, 4],
                "categoria": ["A", "A", "B", "B"],
                "valor": [10, 15, 7, 20],
            }
        )
        df.to_csv(CSV_IN, index=False)

def ingest():
    _seed_example_csv()

def transform():
    if CSV_IN.exists():
        df = pd.read_csv(CSV_IN)
        df = df[df["valor"] > 8]
        agg = df.groupby("categoria", as_index=False)["valor"].sum().rename(columns={"valor": "soma_valor"})
        agg.to_csv(CSV_PROC, index=False)

def export():
    if CSV_PROC.exists():
        df = pd.read_csv(CSV_PROC)
        df.to_csv(CSV_OUT, index=False)
