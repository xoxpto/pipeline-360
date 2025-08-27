from typer.testing import CliRunner
from pipeline_360.cli import app
from pathlib import Path

runner = CliRunner()

def test_cli_clean_cancel(tmp_path):
    data_dir = tmp_path / "data"
    (data_dir / "raw").mkdir(parents=True)
    res = runner.invoke(app, ["--data-dir", str(data_dir), "clean", "--no"])
    assert res.exit_code != 0
    assert data_dir.exists()

def test_cli_run_individual_stages(tmp_path):
    data_dir = tmp_path / "data"
    # ingest
    r1 = runner.invoke(app, ["--data-dir", str(data_dir), "run", "--stage", "ingest"])
    assert r1.exit_code == 0
    assert (data_dir/"raw"/"exemplo.csv").exists()
    # transform
    r2 = runner.invoke(app, ["--data-dir", str(data_dir), "run", "--stage", "transform"])
    assert r2.exit_code == 0
    assert (data_dir/"processed"/"exemplo_proc.csv").exists()
    # export
    r3 = runner.invoke(app, ["--data-dir", str(data_dir), "run", "--stage", "export"])
    assert r3.exit_code == 0
    assert (data_dir/"output"/"resultado.csv").exists()
