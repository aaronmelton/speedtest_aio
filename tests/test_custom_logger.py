"""Unit tests for the Custom Logger Class."""

import logging
import os
from collections.abc import Generator
from datetime import datetime
from pathlib import Path

import pytest

from speedtest_aio.logger.custom_logger import CustomLogger

TEST_LOG_LEVEL = "DEBUG"


@pytest.fixture(name="temp_log_dir")
def fixture_temp_log_dir(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a temporary directory for log files.

    Args:
        tmp_path: pytest's temporary directory fixture.

    Yields:
        Temporary directory path for logs.
    """
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    yield log_dir


@pytest.fixture(name="test_log_config")
def fixture_test_log_config(temp_log_dir: Path) -> dict:
    """Create a test configuration for logging.

    Args:
        temp_log_dir: pytest fixture providing temporary log directory.

    Returns:
        Test logging configuration dictionary.
    """
    return {
        "filename": str(temp_log_dir / f"test_{datetime.now().strftime('%Y%m%d')}.log"),
        "level": TEST_LOG_LEVEL,
        "path": str(temp_log_dir),
    }


@pytest.fixture(autouse=True)
def cleanup_handlers() -> Generator[None, None, None]:
    """Clean up logging handlers after each test."""
    yield
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    logging.Logger.manager.loggerDict.clear()


def test_logger_initialization_creates_default_and_all_loggers(test_log_config: dict) -> None:
    """CustomLogger construction exposes both the "default" and "all" loggers."""
    custom_logger = CustomLogger(log_dict=test_log_config)
    assert isinstance(custom_logger.default, logging.Logger)
    assert isinstance(custom_logger.all, logging.Logger)


def test_log_directory_is_created_when_missing(temp_log_dir: Path, test_log_config: dict) -> None:
    """CustomLogger creates the log directory if it doesn't already exist."""
    temp_log_dir.rmdir()
    assert not temp_log_dir.exists()

    CustomLogger(log_dict=test_log_config)

    assert temp_log_dir.exists()


def test_log_message_is_written_to_configured_file(test_log_config: dict) -> None:
    """Messages logged through `default` land in the configured log file."""
    log_file = Path(test_log_config["filename"])
    test_message = "Test log message"

    custom_logger = CustomLogger(log_dict=test_log_config)
    custom_logger.default.info(test_message)

    assert log_file.exists()
    assert test_message in log_file.read_text(encoding="utf-8")


def test_respects_configured_log_level(test_log_config: dict) -> None:
    """Messages below the configured level are suppressed; at/above are recorded."""
    test_log_config["level"] = "WARNING"
    log_file = Path(test_log_config["filename"])

    custom_logger = CustomLogger(log_dict=test_log_config)
    custom_logger.default.debug("debug message")
    custom_logger.default.warning("warning message")

    content = log_file.read_text(encoding="utf-8")
    assert "debug message" not in content
    assert "warning message" in content


def test_missing_level_key_raises_key_error(temp_log_dir: Path) -> None:
    """A log_dict missing the required "level" key raises KeyError."""
    incomplete_config = {"filename": str(temp_log_dir / "test.log"), "path": str(temp_log_dir)}
    with pytest.raises(KeyError):
        CustomLogger(log_dict=incomplete_config)


def test_missing_path_key_raises_key_error(temp_log_dir: Path) -> None:
    """A log_dict missing the required "path" key raises KeyError."""
    incomplete_config = {"filename": str(temp_log_dir / "test.log"), "level": TEST_LOG_LEVEL}
    with pytest.raises(KeyError):
        CustomLogger(log_dict=incomplete_config)


@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores directory permission bits")
def test_unwritable_log_path_raises_permission_error(tmp_path: Path) -> None:
    """An unwritable LOG_PATH surfaces a PermissionError instead of failing silently."""
    unwritable_dir = tmp_path / "unwritable"
    unwritable_dir.mkdir()
    unwritable_dir.chmod(0o000)
    log_dict = {
        "filename": str(unwritable_dir / "nested" / "test.log"),
        "level": TEST_LOG_LEVEL,
        "path": str(unwritable_dir / "nested"),
    }
    try:
        with pytest.raises(PermissionError):
            CustomLogger(log_dict=log_dict)
    finally:
        unwritable_dir.chmod(0o755)
