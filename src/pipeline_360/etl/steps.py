from pathlib import Path
import pandas as pd
from ..config import Settings  # instanciamos em runtime para apanhar env atual

def _paths():
    # Lê .env e variáveis de ambiente no momento da chamada
    s = Settings()
    data_dir: Path = s.DATA_DIR
    raw = data_dir / "raw"
    proc = data_dir / "processed"
    out = data_dir / "output"
    for d in (raw, proc, out):
        d.mkdir(parents=True, exist_ok=True)
    return raw, proc, out

def _csv_paths():
    raw, proc, out = _paths()
    csv_in = raw / "exemplo.csv"
    csv_proc = proc / "exemplo_proc.csv"
    csv_out = out / "resultado.csv"
    return csv_in, csv_proc, csv_out

def _seed_example_csv(csv_in: Path):
    if not csv_in.exists():
        import pandas as pd
        df = pd.DataFrame(
            {
                "id": [1, 2, 3, 4],
                "categoria": ["A", "A", "B", "B"],
                "valor": [10, 15, 7, 20],
            }
        )
        df.to_csv(csv_in, index=False)

def ingest():
    csv_in, _, _ = _csv_paths()
    _seed_example_csv(csv_in)

def transform():
    csv_in, csv_proc, _ = _csv_paths()
    if csv_in.exists():
        df = pd.read_csv(csv_in)
        # exemplo: filtrar valores > 8 e somar por categoria
        df = df[df["valor"] > 8]
        agg = (
            df.groupby("categoria", as_index=False)["valor"]
            .sum()
            .rename(columns={"valor": "soma_valor"})
        )
        agg.to_csv(csv_proc, index=False)

def export():
    _, csv_proc, csv_out = _csv_paths()
    if csv_proc.exists():
        df = pd.read_csv(csv_proc)
        df.to_csv(csv_out, index=False)
