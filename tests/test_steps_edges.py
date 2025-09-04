import os
from pathlib import Path
from pipeline_360.etl import steps


def test_steps_seed_when_missing(tmp_path, monkeypatch):
    monkeypatch.setenv("DATA_DIR", str(tmp_path / "dataR"))
    # limpar para simular ausência prévia
    raw, proc, _out = (
        Path(os.environ["DATA_DIR"]) / "raw",
        Path(os.environ["DATA_DIR"]) / "processed",
        Path(os.environ["DATA_DIR"]) / "output",
    )
    # apenas export() sem transform -> no-op
    steps.export()
    # transform garante seed se csv_in não existe
    steps.transform()
    assert (raw / "exemplo.csv").exists()
    assert (proc / "exemplo_proc.csv").exists()
