import os
from pathlib import Path
from importlib import reload
import pipeline_360.config as cfg

def test_config_strip_quotes_and_alt_envfile(tmp_path, monkeypatch):
    alt = tmp_path / ".env.alt"
    data_dir = tmp_path / "dataW"
    log_file = tmp_path / "logsW" / "w.log"
    alt.write_text(f'DATA_DIR="{data_dir}"\nLOG_FILE="{log_file}"\nLOG_LEVEL=DEBUG\n', encoding="utf-8")

    monkeypatch.setenv("PIPELINE360_ENV", str(alt))
    reload(cfg)  # reavaliar módulo com novo env
    s = cfg.get_settings()
    assert s.DATA_DIR == data_dir
    assert s.LOG_FILE == log_file
    assert s.LOG_LEVEL == "DEBUG"
