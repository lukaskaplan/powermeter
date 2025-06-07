#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
powermeter_json.py

Script to read current values from Modbus devices using powermeter_core.py
and print them as JSON to stdout.

(Typically used for Zabbix UserParameter or manual testing.)
"""

import json
import sys
from powermeter import get_values

CONFIG_PATH = '/etc/powermeter/powermeter_config.json'

if len(sys.argv) > 1:
    CONFIG_PATH = sys.argv[1]

values = get_values(CONFIG_PATH)
print(json.dumps(values, indent=4))
