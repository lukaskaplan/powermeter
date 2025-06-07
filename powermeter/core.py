#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
powermeter/core.py

Core module for Powermeter.

Provides get_values() function to read current values from Modbus devices
based on configuration.
"""

import json
import logging
from pymodbus.client import ModbusSerialClient


def get_values(config_path):
    """
    Read current values from configured Modbus devices.

    Parameters:
        config_path (str): Path to the JSON configuration file.

    Returns:
        List[Dict]: List of dictionaries with keys:
            - id (int)
            - device_id (int)
            - input (str)
            - name (str)
            - current (float)
    """

    # Load configuration from JSON file
    with open(config_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    results = []
    unique_id = 0   # Used as unique index 'id' for values in the output

    # Iterate over all configured devices
    for device in data:

        # Initialize Modbus RTU client for this device
        modbusclient = ModbusSerialClient(
            port = str(device["port"]),
            timeout = int(device["timeout"]),
            stopbits = int(device["stopbits"]),
            bytesize = int(device["bytesize"]),
            parity = str(device["parity"]),
            baudrate = int(device["baudrate"])
        )

        # Attempt to connect to the device
        connection = modbusclient.connect()
        if not connection:
            logging.warning(
                "Device ID %s on port %s - connection failed!",
                device['id'],
                device['port']
            )
            continue    # Skip to next device if connection failed

        try:
            # Read 16 holding registers starting at address 8
            request = modbusclient.read_holding_registers(address=8, count=16)

            # Check for Modbus read error
            if request.isError():
                logging.warning(
                    "Device ID %s - Modbus read error!",
                    device['id']
                )
                modbusclient.close()
                continue

            # Convert Modbus registers to float values
            current_values = [float(request.registers[i]) for i in range(16)]

            # For each configured input on this device
            for idx, inp in enumerate(device["inputs"]):
                # Apply scaling ratio
                current = current_values[idx] * inp["ratio"]
                current = round(current, 2)

                # Append result dictionary for this input
                results.append({
                    "id": unique_id,
                    "device_id": device["id"],
                    "input": inp["input"],
                    "name": inp["name"],
                    "current": current
                })
                unique_id += 1  # Increment unique ID for next input

        except Exception as e:   # pylint: disable=broad-exception-caught
            logging.error(
                "Device ID %s - Exception: %s",
                device['id'], e
            )

        finally:
            # Close the Modbus connection
            modbusclient.close()

    # Return the full list of results for all devices and inputs
    return results
