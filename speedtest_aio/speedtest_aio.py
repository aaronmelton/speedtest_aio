"""Speedtest Monitor."""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import json
import sqlite3
import subprocess
import sys
from datetime import datetime
from time import perf_counter

from aaron_common_libs.common_funcs import pretty_print
from aaron_common_libs.logger.custom_logger import CustomLogger
from config import Config

config = Config()
logging_handler = CustomLogger(log_dict=config.log_dict)
logger = logging_handler.default
logger_all = logging_handler.all


def create_database(db_filename):
    """Check for presence of database.  Create it (and/or table) if necessary.

    Args
    ----
    db_filename: str

    Returns
    -------
    output_json : str
    """
    logger.debug("START")
    logger.debug("db_filename=='%s'", db_filename)
    result = False
    create_file = False
    database_connection = sqlite3.connect(db_filename)
    # Don't need to check for the presence of db_filename; If it doesn't exist
    # the sqlite3.connect() will create it.  We do need to check for the table.
    logger.info("Database file exists; Checking for correct table...")
    this_query = """SELECT name FROM sqlite_master WHERE type='table' AND name='speedtest'"""
    check_table = db_query(db_filename=db_filename, query=this_query, some_list=None)
    if not check_table:
        logger.warning("Database table not found.")
        create_file = True
    else:
        if "speedtest" in check_table[0]:
            logger.info("Found database table.")
            result = True
        else:
            logger.warning("Database table not found.")
            create_file = True

    if create_file:
        logger.warning("Database file and/or table does not exist; Attempting to create...")
        try:
            cursor = database_connection.cursor()
            cursor.execute(
                """CREATE TABLE speedtest (test_id integer primary key autoincrement, timestamp integer, download integer, upload integer, ping float, server_id integer, server_host text)"""
            )
            database_connection.commit()
            logger.info("Database created successfully!")
            database_connection.close()
            result = True
        except Exception as some_exception:  # pylint: disable=broad-except
            logger.error("ERROR creating new database or committing changes.")
            logger.exception("ERROR=='%s'", some_exception)
    logger.debug("STOP")
    return result


def db_query(db_filename, query, some_list):
    """Query database and return results.

    Args
    ----
    db_filename : str
    query : str
    some_list : dict

    Returns
    -------
    output_json : str
    """
    logger.debug("START")
    logger.debug("db_filename=='%s'", db_filename)
    logger.debug("query=='%s'", query)
    logger.debug("some_list=='%s'", some_list)
    output_json = []
    database_connection = sqlite3.connect(db_filename)
    cursor = database_connection.cursor()

    if some_list:
        try:
            try:
                logger.info("Writing changes to database...")
                cursor.execute(query, some_list)
                logger.info("Database write successful.")
            except Exception as some_exception:  # pylint: disable=broad-except
                logger.error("ERROR running query.")
                logger.exception("ERROR=='%s'", some_exception)
            try:
                database_connection.commit()
            except Exception as some_exception:  # pylint: disable=broad-except
                logger.exception("ERROR=='%s'", some_exception)
                logger.error("ERROR committing changes.")
        except Exception as some_exception:  # pylint: disable=broad-except
            logger.error("ERROR running query: %s", str(query))
            logger.exception("ERROR=='%s'", some_exception)

    # If some_list is NOT provided, this query will be retrieving data
    # from the database.
    if not some_list:
        # This script doesn't query the db so this functionality hasn't been
        # checked against SQLite syntax (it was adapted from MySQL)
        try:
            logger.info("Querying database...")
            cursor.execute(query)
            output_json = cursor.fetchall()
            logger.info("Database query successful.")
        except Exception as some_exception:  # pylint: disable=broad-except
            logger.error("ERROR running query: %s", str(query))
            logger.exception("ERROR=='%s'", some_exception)
    cursor.close()

    logger.debug("STOP")
    return output_json


def main():
    """Main Function.

    Args
    ----

    Returns
    -------
    None
    """
    start_time = perf_counter()

    logger.info("")
    logger_all.info("---------- START START START ----------")
    logger_all.info(
        "%s v%s (%s)",
        config.app_dict["title"],
        config.app_dict["version"],
        config.app_dict["date"],
    )

    logger.info("Running speedtest...")
    try:
        process = subprocess.run(["/usr/local/bin/speedtest", "--json"], check=True, capture_output=True)
        speedtest_results = json.loads(process.stdout.decode("utf-8"))
        logger.debug("speedtest_results==%s", pretty_print(speedtest_results))
        logger.info("Speedtest run successfully.")
    except Exception as some_exception:  # pylint: disable=broad-except
        speedtest_results = None
        logger.error("ERROR running speed test.")
        logger.exception("EXCEPTION='%s'", str(some_exception))

    if speedtest_results:
        database_filename = "/app/db/speedtest_database.sqlite"
        speedtest_list = {}

        # Need to convert datetime/timestamp to epoch int; Works better with Grafana
        utc_time = datetime.strptime(speedtest_results["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
        epoch_time = (utc_time - datetime(1970, 1, 1)).total_seconds()

        speedtest_list["timestamp"] = int(epoch_time)
        speedtest_list["download"] = speedtest_results["download"]
        speedtest_list["upload"] = speedtest_results["upload"]
        speedtest_list["ping"] = speedtest_results["ping"]
        speedtest_list["server_id"] = speedtest_results["server"]["id"]
        speedtest_list["server_host"] = speedtest_results["server"]["host"]

        if create_database(database_filename):
            this_query = """INSERT INTO speedtest (timestamp, download, upload, ping, server_id, server_host) VALUES (:timestamp, :download, :upload, :ping, :server_id, :server_host)"""
            # Convert dict to list to work with SQLite
            speedtest_values = [int(x) if isinstance(x, bool) else x for x in speedtest_list.values()]
            try:
                db_query(db_filename=database_filename, query=this_query, some_list=speedtest_values)
            except Exception as some_exception:  # pylint: disable=broad-except
                logger.error("ERROR running db_query")
                logger.exception("EXCEPTION='%s'", str(some_exception))
    else:
        logger.error("Error running speed test.")

    logger_all.info("Total Execution Time: %s seconds", round(perf_counter() - start_time, 2))
    logger_all.info("----------   STOP STOP STOP  ----------")
    logger.info("")


if __name__ == "__main__":
    sys.exit(main())
