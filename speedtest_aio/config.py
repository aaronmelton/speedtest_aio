"""Config file required to support Speedtest Monitor."""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

from dataclasses import dataclass
from datetime import datetime
from os import environ as os_environ


@dataclass
class Config:
    """Class for Application variables."""

    def __init__(self) -> None:
        """Application Variables."""
        self.app_dict = {
            "author": "Aaron Melton <aaron@aaronmelton.com>",
            "date": "2026-07-28",
            "desc": "A Python script to capture speedtest JSON and insert it into a database.",
            "title": "speedtest_aio",
            "url": "https://github.com/aaronmelton/speedtest_aio",
            "version": "0.9.0",
        }

        # Logging Variables
        self.log_dict = {
            "filename": f"""{os_environ.get("LOG_PATH", "log/")}{self.app_dict["title"]}_{datetime.now().strftime("%Y%m%d")}.log""",
            "level": os_environ.get("LOG_LEVEL", "INFO"),
            "path": os_environ.get("LOG_PATH", "log/"),
        }
