from typer.testing import CliRunner
from pipeline_360.cli import app

runner = CliRunner()


def test_cli_global_flags_and_clean(tmp_path, monkeypatch):
    data_dir = tmp_path / "dataZ"
    log_file = tmp_path / "logsZ" / "z.log"

    # run com overrides globais
    r = runner.invoke(
        app,
        [
            "--data-dir",
            str(data_dir),
            "--log-file",
            str(log_file),
            "--log-level",
            "DEBUG",
            "run",
            "--stage",
            "all",
        ],
    )
    assert r.exit_code == 0
    assert (data_dir / "raw" / "exemplo.csv").exists()
    assert log_file.exists()

    # clean sem prompt
    r2 = runner.invoke(
        app,
        ["--data-dir", str(data_dir), "--log-file", str(log_file), "clean", "--yes"],
    )
    assert r2.exit_code == 0
    assert not data_dir.exists()
    assert not log_file.exists()


def test_cli_config_alt_envfile(tmp_path):
    # .env com caminhos citados
    env_alt = tmp_path / ".env.alt"
    data_dir = tmp_path / "dataQ"
    log_file = tmp_path / "logsQ" / "q.log"
    env_alt.write_text(
        f'DATA_DIR="{data_dir}"\nLOG_FILE="{log_file}"\nLOG_LEVEL=DEBUG\n',
        encoding="utf-8",
    )

    r = runner.invoke(app, ["--config", str(env_alt), "run", "--stage", "all"])
    assert r.exit_code == 0
    assert (data_dir / "raw" / "exemplo.csv").exists()
    assert log_file.exists()
