#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
powermeter_influx.py

Script to periodically read values from HDHK devices and send them to InfluxDB.

Can be used as a systemd service for continuous data collection.
"""

import logging
import time
import sys
import os
from configparser import ConfigParser

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.rest import ApiException

from powermeter import get_values

# Configuration files
INFLUX_CONFIG_FILE = "/etc/powermeter/influx.conf"
POWERMETER_CONFIG_FILE = "/etc/powermeter/powermeter.json"

# ------------------------------------------------------------------------------
# Configure the logger
# ------------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Powermeter starts.")

# ------------------------------------------------------------------------------
# Check that configuration files exist
# ------------------------------------------------------------------------------

if not os.path.isfile(INFLUX_CONFIG_FILE):
    logging.error("Influx config file not found: %s", INFLUX_CONFIG_FILE)
    sys.exit(1)

if not os.path.isfile(POWERMETER_CONFIG_FILE):
    logging.error("Powermeter config file not found: %s", POWERMETER_CONFIG_FILE)
    sys.exit(1)

# ------------------------------------------------------------------------------
# Read InfluxDB configuration
# ------------------------------------------------------------------------------

config_object = ConfigParser()
config_object.read(INFLUX_CONFIG_FILE)
influx = config_object["influx"]
token = influx["token"]
org = influx["org"]
url = influx["url"]
bucket = influx["bucket"]
verify_ssl = config_object.getboolean("influx", "verify_ssl")

# ------------------------------------------------------------------------------
# Initialize InfluxDB client and test connectivity
# ------------------------------------------------------------------------------

try:
    logging.info("Initializing InfluxDB client for %s", url)
    client = InfluxDBClient(url=url, token=token, org=org, verify_ssl=verify_ssl)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    # Test connection (DNS, TCP, SSL)
    logging.info("Pinging InfluxDB server to verify connectivity...")
    if not client.ping():
        logging.error("Failed to ping InfluxDB server at %s", url)
        sys.exit(1)
    else:
        logging.info("Ping OK.")
except Exception as e:  # pylint: disable=broad-exception-caught
    logging.error("Failed to initialize or ping InfluxDB client: %s", e)
    sys.exit(1)

# ------------------------------------------------------------------------------
# Main data collection loop
# ------------------------------------------------------------------------------

logging.info("Start collecting data")

try:
    while True:
        # Read current values from Powermeter (HDHK devices)
        values = get_values(POWERMETER_CONFIG_FILE)

        for item in values:
            # Create InfluxDB Point
            point = (
                Point(influx["measurement"])
                .tag("device_id", str(item["device_id"]))
                .tag("input", item["input"])
                .tag("name", item["name"])
                .tag("unique_id", str(item["id"]))
                .field("current", float(item["current"]))
            )

            # Write point to InfluxDB
            try:
                write_api.write(bucket=influx["bucket"], org=influx["org"], record=point)
            except ApiException as e:
                if e.status == 401:
                    logging.error("Unauthorized (401): Bad token for InfluxDB.")
                elif e.status == 404:
                    logging.error(
                        "Not Found (404): Organization or bucket not found in InfluxDB."
                        "Check 'org' and 'bucket' in config."
                    )
                else:
                    logging.error("InfluxDB ApiException: %s", e)
                sys.exit(1)

        # Wait before the next measurement cycle
        time.sleep(int(influx["interval"]))

# ------------------------------------------------------------------------------
# Graceful shutdown
# ------------------------------------------------------------------------------

except KeyboardInterrupt:
    logging.info("Stopping powermeter influx loop (Ctrl+C)")

finally:
    client.close()
    logging.info("InfluxDB client closed")
