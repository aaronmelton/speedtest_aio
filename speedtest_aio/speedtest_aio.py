"""Speedtest Monitor."""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import json
import logging
import sqlite3
import subprocess
import sys
from datetime import date, datetime
from time import time

from config import app_dict


def create_database(db_filename):
    """Check for presence of database.  Create it (and/or table) if necessary.

    Args
    ----
    db_deets: dict

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
    query = """SELECT name FROM sqlite_master WHERE type='table' AND name='speedtest'"""
    check_table = db_query("/var/lib/db/speedtest_database.sqlite", query, None)
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
        logger.info("Database file and/or table does not exist; Attempting to create...")
        try:
            cursor = database_connection.cursor()
            cursor.execute(
                """CREATE TABLE speedtest (
                            test_id integer primary key autoincrement,
                            datetime text,
                            timestamp integer,
                            ping_jitter float,
                            ping_latency float,
                            download_bandwidth integer,
                            download_bytes integer,
                            download_elapsed integer,
                            upload_bandwidth integer,
                            upload_bytes integer,
                            upload_elapsed integer,
                            packetloss integer,
                            server_id integer,
                            server_host text,
                            server_port integer,
                            server_name text,
                            server_location text,
                            server_country text,
                            server_ip text)"""
            )
            database_connection.commit()
            logger.info("Database created successfully!")
            database_connection.close()
            result = True
        except Exception as some_exception:
            logger.error("ERROR creating new database or committing changes.")
            logger.exception("ERROR=='%s'", some_exception)
    logger.debug("STOP")
    return result


def db_query(db_filename, query, some_list):
    """Query database and return results.

    Args
    ----
    db_deets["filename"] : str
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
            except Exception as some_exception:
                logger.error("ERROR running query.")
                logger.exception("ERROR=='%s'", some_exception)
            try:
                database_connection.commit()
            except Exception as some_exception:
                logger.exception("ERROR=='%s'", some_exception)
                logger.error("ERROR committing changes.")
        except Exception as some_exception:
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
        except Exception as some_exception:
            logger.error("ERROR running query: %s", str(query))
            logger.exception("ERROR=='%s'", some_exception)
    cursor.close()

    logger.debug("STOP")
    return output_json


def pretty_print(this_string):
    """Return a nicely-formatted JSON string.

    Args
    ----
    this_string : str

    Returns
    -------
    : str
    """
    return json.dumps(this_string, indent=4)


def main():
    """Main Function.

    Args
    ----
    None

    Returns
    -------
    None
    """
    start_time = time()

    # Setup Logging Functionality
    logging.basicConfig(
        # pylint: disable=line-too-long
        filename=f"""/var/log/speedtest_aio_{date.today().strftime("%Y%m%d")}.log""",
        filemode="a",
        format="{asctime}  Log Level: {levelname:8}  Line: {lineno:4}  Function: {funcName:21}  Msg: {message}",
        style="{",
        datefmt="%Y-%m-%dT%H:%M:%S",
        level="INFO",
    )

    logger.info("START START START")
    logger.info(
        "%s %s (%s)",
        app_dict["name"],
        app_dict["version"],
        app_dict["date"],
    )

    logger.info("Running speedtest...")
    try:
        process = subprocess.run(
            ["/usr/bin/speedtest", "--accept-license", "-f", "json"], check=True, capture_output=True
        )
        speedtest_results = json.loads(process.stdout.decode("utf-8"))
        logger.debug("speedtest_results==%s", pretty_print(speedtest_results))

    except Exception as some_exception:
        speedtest_results = None
        logger.error("ERROR running speed test.")
        logger.exception("EXCEPTION='%s'", str(some_exception))

    if speedtest_results is not None:
        speedtest_list = {}
        speedtest_list["datetime"] = speedtest_results["timestamp"]

        # Need to convert datetime/timestamp to epoch int; Works better with Grafana
        utc_time = datetime.strptime(speedtest_list["datetime"], "%Y-%m-%dT%H:%M:%SZ")
        epoch_time = (utc_time - datetime(1970, 1, 1)).total_seconds()

        speedtest_list["timestamp"] = int(epoch_time)
        speedtest_list["ping_jitter"] = speedtest_results["ping"]["jitter"]
        speedtest_list["ping_latency"] = speedtest_results["ping"]["latency"]
        speedtest_list["download_bandwidth"] = speedtest_results["download"]["bandwidth"]
        speedtest_list["download_bytes"] = speedtest_results["download"]["bytes"]
        speedtest_list["download_elapsed"] = speedtest_results["download"]["elapsed"]
        speedtest_list["upload_bandwidth"] = speedtest_results["upload"]["bandwidth"]
        speedtest_list["upload_bytes"] = speedtest_results["upload"]["bytes"]
        speedtest_list["upload_elapsed"] = speedtest_results["upload"]["elapsed"]
        speedtest_list["packetloss"] = speedtest_results["packetLoss"]
        speedtest_list["server_id"] = speedtest_results["server"]["id"]
        speedtest_list["server_host"] = speedtest_results["server"]["host"]
        speedtest_list["server_port"] = speedtest_results["server"]["port"]
        speedtest_list["server_name"] = speedtest_results["server"]["name"]
        speedtest_list["server_location"] = speedtest_results["server"]["location"]
        speedtest_list["server_country"] = speedtest_results["server"]["country"]
        speedtest_list["server_ip"] = speedtest_results["server"]["ip"]

        if create_database("/var/lib/db/speedtest_database.sqlite"):
            db_columns = ", ".join(speedtest_list.keys())
            db_placeholders = ", ".join("?" * len(speedtest_list))
            query = f"""INSERT INTO speedtest ({db_columns}) VALUES ({db_placeholders})"""
            # Convert dict to list to work with SQLite
            speedtest_values = [int(x) if isinstance(x, bool) else x for x in speedtest_list.values()]

            try:
                db_query("/var/lib/db/speedtest_database.sqlite", query, speedtest_values)
            except Exception as some_exception:
                logger.error("ERROR running db_query")
                logger.exception("EXCEPTION='%s'", str(some_exception))
    else:
        logger.error("Error running speed test.")

    logger.info("Total Execution Time: %s seconds", time() - start_time)
    logger.info("STOP STOP STOP")
    return 0


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    sys.exit(main())
