from pathlib import Path
from typer.testing import CliRunner
from pipeline_360.cli import app

runner = CliRunner()

def test_cli_run_with_flags_and_clean(tmp_path):
    data_dir = tmp_path / "data"
    log_file = tmp_path / "logs" / "x.log"

    # run all with overrides
    res = runner.invoke(app, ["--data-dir", str(data_dir), "--log-file", str(log_file), "--log-level", "DEBUG", "run", "--stage", "all"])
    assert res.exit_code == 0, res.stdout

    # artefactos criados
    assert (data_dir / "raw" / "exemplo.csv").exists()
    assert (data_dir / "processed" / "exemplo_proc.csv").exists()
    assert (data_dir / "output" / "resultado.csv").exists()
    assert log_file.exists()

    # clean
    res2 = runner.invoke(app, ["--data-dir", str(data_dir), "--log-file", str(log_file), "clean", "--yes"])
    assert res2.exit_code == 0, res2.stdout
    assert not data_dir.exists()
    assert not log_file.exists()
