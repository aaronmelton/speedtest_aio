"""Test db_query parameter binding."""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sqlite3
import warnings
from pathlib import Path

import pytest

from speedtest_aio.speedtest_aio import db_query

INSERT_NAMED = (
    "INSERT INTO speedtest (timestamp, download, upload, ping, server_id, server_host) "
    "VALUES (:timestamp, :download, :upload, :ping, :server_id, :server_host)"
)

SAMPLE_ROW = {
    "timestamp": 1785038051,
    "download": 943210000.0,
    "upload": 41230000.0,
    "ping": 12.345,
    "server_id": "1234",
    "server_host": "speedtest.example.net:8080",
}


@pytest.fixture(name="db_path")
def fixture_db_path(tmp_path: Path) -> str:
    """Create an empty speedtest table and return its path."""
    path = str(tmp_path / "speedtest.db")
    connection = sqlite3.connect(path)
    connection.execute(
        "CREATE TABLE speedtest (timestamp INTEGER, download REAL, upload REAL, "
        "ping REAL, server_id TEXT, server_host TEXT)"
    )
    connection.commit()
    connection.close()
    return path


def test_named_placeholders_bind_from_a_dict(db_path: str) -> None:
    """A dict binds to named placeholders and the row round-trips intact."""
    db_query(db_filename=db_path, query=INSERT_NAMED, params=SAMPLE_ROW)

    connection = sqlite3.connect(db_path)
    stored = connection.execute(
        "SELECT timestamp, download, upload, ping, server_id, server_host FROM speedtest"
    ).fetchall()
    connection.close()

    assert stored == [tuple(SAMPLE_ROW.values())]


def test_named_placeholders_emit_no_deprecation_warning(db_path: str) -> None:
    """Binding a dict raises no DeprecationWarning.

    Passing a sequence to a named-placeholder query warns on Python 3.12/3.13 and
    raises sqlite3.ProgrammingError on 3.14. This guards the fix from regressing.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        db_query(db_filename=db_path, query=INSERT_NAMED, params=SAMPLE_ROW)


def test_booleans_bind_as_integers(db_path: str) -> None:
    """SQLite has no bool type; a bool bound to an INTEGER column lands as 0/1."""
    row = {**SAMPLE_ROW, "timestamp": True}
    db_query(db_filename=db_path, query=INSERT_NAMED, params=row)

    connection = sqlite3.connect(db_path)
    stored = connection.execute("SELECT timestamp FROM speedtest").fetchone()
    connection.close()

    assert stored == (1,)


def test_read_path_takes_no_params(db_path: str) -> None:
    """params=None selects the read path and returns rows."""
    db_query(db_filename=db_path, query=INSERT_NAMED, params=SAMPLE_ROW)

    rows = db_query(
        db_filename=db_path,
        query="SELECT server_host FROM speedtest",
        params=None,
    )

    assert rows == [("speedtest.example.net:8080",)]
