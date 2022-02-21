#!/bin/sh

# Run the script one time to populate the database so we won't have any empty
# dashboard in Grafana
/usr/local/bin/python /app/speedtest_aio.py

# Using Supercronic to run crontab as docker user
/usr/bin/supercronic /app/crontab
