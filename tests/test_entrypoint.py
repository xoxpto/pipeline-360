import runpy
import sys

def test_entrypoint_module_help():
    sys.argv = ["pipeline_360", "--help"]
    try:
        runpy.run_module("pipeline_360", run_name="__main__")
    except SystemExit as e:
        # Typer termina com 0 quando imprime --help
        assert e.code == 0
