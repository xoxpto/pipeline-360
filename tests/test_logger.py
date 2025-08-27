from pathlib import Path
import os
from pipeline_360.logger import setup_logging, get_logger

def test_logger_file_created(tmp_path, monkeypatch):
    log_dir = tmp_path / "logs"
    log_file = log_dir / "test.log"
    monkeypatch.setenv("LOG_FILE", str(log_file))
    setup_logging(level="INFO", log_file=log_file)
    lg = get_logger("t")
    lg.info("linha")
    assert log_file.exists()
    contents = log_file.read_text(encoding="utf-8")
    assert "linha" in contents
