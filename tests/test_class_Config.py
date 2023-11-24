"""Test class Config."""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pylint: disable=invalid-name, duplicate-code

from re import match as re_match
from speedtest_aio.config import Config


def test_config():
    """Test config.py"""
    config = Config()
    # Application Variables
    assert config.app_dict["author"] == "Aaron Melton <aaron@aaronmelton.com>"
    assert re_match("\\d{4}(-\\d{2}){2}", config.app_dict["date"])
    assert config.app_dict["desc"] == "A Python script to capture speedtest JSON and insert it into a database."
    assert config.app_dict["title"] == "speedtest_aio"
    assert config.app_dict["url"] == "https://github.com/aaronmelton/speedtest_aio"
    assert re_match("\\d{1,2}(\\.\\d{1,2}){2}", config.app_dict["version"])

    # Logging Variables
    assert config.log_dict["level"] == "DEBUG"
