import pandas as pd


def test_pipeline_end_to_end(tmp_path, monkeypatch):
    # usar diretório de dados temporário
    data_dir = tmp_path / "data"
    monkeypatch.setenv("DATA_DIR", str(data_dir))

    # correr pipeline por etapas
    from pipeline_360.etl.pipeline import run_pipeline

    run_pipeline("all")

    raw = data_dir / "raw" / "exemplo.csv"
    proc = data_dir / "processed" / "exemplo_proc.csv"
    out = data_dir / "output" / "resultado.csv"

    assert raw.exists()
    assert proc.exists()
    assert out.exists()

    # validar conteúdo processado
    df = pd.read_csv(proc)
    assert set(df.columns) == {"categoria", "soma_valor"}
    # como filtramos valor > 8, a categoria B só tem 20, A tem 25
    got = {row["categoria"]: row["soma_valor"] for _, row in df.iterrows()}
    assert got == {"A": 25, "B": 20}
