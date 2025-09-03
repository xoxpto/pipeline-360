import pandas as pd
from ..config import DATA_DIR
from ..logger import get_logger

log = get_logger(__name__)


def _ensure_dirs():
    (DATA_DIR / "raw").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "processed").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "output").mkdir(parents=True, exist_ok=True)


def ingest():
    _ensure_dirs()
    raw_csv = DATA_DIR / "raw" / "exemplo.csv"
    if not raw_csv.exists():
        df = pd.DataFrame(
            {
                "id": [1, 2, 3, 4],
                "categoria": ["A", "B", "A", "B"],
                "valor": [10, 20, 5, 7],
                "valor2": [1, 2, 3, 4],
            }
        )
        df.to_csv(raw_csv, index=False)
    log.info("Ingest concluído")


def transform():
    _ensure_dirs()
    raw_csv = DATA_DIR / "raw" / "exemplo.csv"
    if not raw_csv.exists():
        ingest()
    df = pd.read_csv(raw_csv)

    if "categoria" in df.columns and "valor" in df.columns:
        dfp = (
            df.groupby("categoria", as_index=False)["valor"]
            .sum()
            .rename(columns={"valor": "soma_valor"})
        )
    else:
        # fallback (não esperado pelos testes, mas robusto)
        dfp = df

    proc_csv = DATA_DIR / "processed" / "exemplo_proc.csv"
    dfp.to_csv(proc_csv, index=False)
    log.info(f"Transform concluído: {proc_csv}")


def export():
    _ensure_dirs()
    proc_csv = DATA_DIR / "processed" / "exemplo_proc.csv"
    if not proc_csv.exists():
        transform()
    df = pd.read_csv(proc_csv)
    out_csv = DATA_DIR / "output" / "resultado.csv"
    df.to_csv(out_csv, index=False)
    log.info(f"Export concluído: {out_csv}")
