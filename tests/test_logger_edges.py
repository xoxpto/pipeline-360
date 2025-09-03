from pipeline_360.logger import setup_logging, get_logger
import logging


def test_logger_console_only(tmp_path, monkeypatch, caplog):
    # forçar falha de FileHandler (nome inválido em Windows/posix)
    bad_path = "?:/\\invalid\\log.txt"
    setup_logging(
        level="INFO", log_file=bad_path
    )  # deve cair para consola sem rebentar
    log = get_logger("x")
    with caplog.at_level(logging.INFO):
        log.info("msg")
    assert any("msg" in r.message for r in caplog.records)


def test_logger_reconfigure_closes_handlers(tmp_path):
    log1 = tmp_path / "a.log"
    setup_logging(level="INFO", log_file=log1)
    log = get_logger("y")
    log.info("first")
    # reconfigurar para outro ficheiro (tem de fechar o anterior)
    log2 = tmp_path / "b.log"
    setup_logging(level="DEBUG", log_file=log2)
    log.debug("second")
    assert log1.exists()
    assert log2.exists()
