#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
scripts/powermeter_json.py

This script reads current values from Modbus devices using powermeter python package
and prints the results as formated JSON to stdout.

Usage:
    ./powermeter_json.py [config_file]

If a config file path is provided as an argument, it will be used.
Otherwise, the default path '/etc/powermeter/powermeter.json' is used.

This is typically used for Zabbix UserParameter integration or manual testing.
"""

import json
import sys
from powermeter import get_values

CONFIG_PATH = '/etc/powermeter/powermeter.json'

if len(sys.argv) > 1:
    CONFIG_PATH = sys.argv[1]

values = get_values(CONFIG_PATH)
print(json.dumps(values, indent=4))
