from typer.testing import CliRunner
from pipeline_360.cli import app

runner = CliRunner()

def test_cli_hello():
    res = runner.invoke(app, ["hello", "--name", "André"])
    assert res.exit_code == 0
    assert "Olá" in res.stdout

def test_cli_run_help():
    res = runner.invoke(app, ["--help"])
    assert res.exit_code == 0
    assert "CLI do Pipeline 360" in res.stdout
