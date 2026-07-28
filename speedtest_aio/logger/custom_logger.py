"""Aaron's Custom Logging Class."""

from json import dumps as json_dumps
from logging import Logger, getLogger
from logging.config import dictConfig
from pathlib import Path


class CustomLogger:
    """Class for custom logging destinations."""

    def __init__(self, log_dict: dict) -> None:
        """Initialize this class.

        Args:
            log_dict: Logging configuration dictionary containing:
                filename (str): Path to log file
                level (str): Logging level (e.g., "INFO", "DEBUG")
                path (str): Directory path for log files
                format (str, optional): Custom log format string
                formatter (str, optional): Formatter type ("default" or "json")
        """
        # Get format configuration from log_dict or use defaults
        default_format = (
            "{asctime}  Log Level: {levelname:8}  Line: {lineno:4}  Function: {funcName:29}  Msg: {message}"
        )
        json_format = json_dumps(
            {
                "time": "%(asctime)s",
                "level": "%(levelname)s",
                "name": "%(name)s",
                "line": "%(lineno)s",
                "function": "%(funcName)s",
                "message": "%(message)s",
            }
        )

        # Determine which formatter to use
        formatter_type = log_dict.get("formatter", "default")
        log_format = log_dict.get("format", json_format if formatter_type == "json" else default_format)

        logging_config = {
            "version": 1,
            "formatters": {
                "default": {
                    "format": log_format,
                    "style": "{" if "{" in log_format else "%",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                },
            },
            "handlers": {
                "console": {
                    "level": "ERROR",
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stdout",
                },
                "file": {
                    "level": log_dict["level"],
                    "class": "logging.FileHandler",
                    "formatter": "default",
                    "filename": log_dict["filename"],
                },
            },
            "loggers": {
                "": {  # Root logger
                    "level": log_dict["level"],
                    "handlers": ["console", "file"],
                    "propagate": True,
                },
                "all": {
                    "level": log_dict["level"],
                    "handlers": ["console", "file"],
                    "propagate": False,
                },
                "default": {
                    "level": log_dict["level"],
                    "handlers": ["console", "file"],
                    "propagate": False,
                },
            },
            "disable_existing_loggers": False,
        }

        self.all = self.configure_logger(name="all", log_config=logging_config, log_dict=log_dict)
        self.default = self.configure_logger(name="default", log_config=logging_config, log_dict=log_dict)

    def configure_logger(self, name: str, log_config: dict, log_dict: dict) -> Logger:
        """Configure multiple logging destinations.

        Args:
            name: Name of the logging handler (all, default, etc).
            log_config: Custom logging handler configuration.
            log_dict: Logging configuration dictionary.

        Returns:
            Configured logger instance
        """
        Path(log_dict["path"]).mkdir(parents=True, exist_ok=True)
        dictConfig(config=log_config)
        return getLogger(name=name)
