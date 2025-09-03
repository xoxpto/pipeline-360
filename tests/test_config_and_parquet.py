from pathlib import Path
from typer.testing import CliRunner
from pipeline_360.cli import app

runner = CliRunner()

def test_cli_with_config_envfile(tmp_path):
    env_alt = tmp_path / ".env.alt"
    data_dir = tmp_path / "dataX"
    log_file = tmp_path / "logsX" / "alt.log"

    # ★ Colocar os caminhos ENTRE ASPAS para evitar problemas com backslashes no Windows
    env_alt.write_text(
        f'DATA_DIR="{data_dir}"\nLOG_FILE="{log_file}"\nLOG_LEVEL=DEBUG\n',
        encoding="utf-8",
    )

    res = runner.invoke(app, ["--config", str(env_alt), "run", "--stage", "all"])
    assert res.exit_code == 0, res.stdout

    assert (data_dir / "raw" / "exemplo.csv").exists()
    assert (data_dir / "processed" / "exemplo_proc.csv").exists()
    assert (data_dir / "output" / "resultado.csv").exists()
    assert log_file.exists()
