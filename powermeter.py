################################################################
##                                                            ##
##                       Powermeter                           ##
##                                                            ##
## Description:                                               ##
##     This simple script reads current values                ##
##     from Chinese HDHK current meter via RS485 ModBUS-RTU   ##
##     and then send them to remote InfluxDB. Data can be     ##
##     simply visualised by Grafana.                          ##
## Author: Lukas Kaplan                                       ##
## Email: lukas.kaplan@lkaplan.cz                             ##
## License: BSD                                               ##
## Version: 1.1                                               ##
################################################################

import sys
import time # for sleep(interval) 
import datetime # for influxdb timestamp
from influxdb import InfluxDBClient
from pymodbus.client import ModbusSerialClient as ModbusClient
from configparser import ConfigParser
  
### Read the config file ###
config_object = ConfigParser()
config_object.read("/etc/powermeter.conf")
influx = config_object["influx"]
modbus = config_object["modbus"]
ratio = config_object["ratio"]
loop = config_object["loop"]

# List of HDHK Current meter input names
interface = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p"]

### ModBUS ###
modbusclient = ModbusClient(
    #method = modbus["method"], 
    port = modbus["port"], 
    timeout = int(modbus["timeout"]), 
    stopbits = int(modbus["stopbits"]), 
    bytesize = int(modbus["bytesize"]),  
    parity=modbus["parity"], 
    baudrate = int(modbus["baudrate"])
)
modbusclient.connect()

### INFLUX ###
# Create the InfluxDB client object
influxclient = InfluxDBClient(
    host=influx["host"],
    port=influx["port"],
    username=influx["user"],
    password=influx["password"],
    database=influx["dbname"],
    ssl=bool(influx["ssl"]),
    verify_ssl=bool(influx["verify_ssl"])   
)

### ONESHOT MODE ###
if len(sys.argv) > 1:
#    if str(sys.argv[1]) == "-oneshot":
    request = modbusclient.read_holding_registers(address=0,count=56,slave=1)
    for i in range(0,len(interface)):
        current = float(ratio[interface[i]]) * request.registers[8+i]
        current = round(current, 2)
        if str(sys.argv[1]) == interface[i]:
            # print(interface[i], current, "A")
            print(current)
            break

### DAEMON MODE ###
else:
    # Run until you get a ctrl^c
    try:
        while True:
            timestamp=datetime.datetime.utcnow().isoformat()
            request = modbusclient.read_holding_registers(address=0,count=56,slave=1)
            #print(request.registers)
    
            for i in range(0,len(interface)):
                current = float(ratio[interface[i]]) * request.registers[8+i]
                current = round(current, 2)
                print(interface[i], current, "A")
                # Create the JSON data structure
                data = [
                {
                  "measurement": influx["measurement"],
                      "tags": {
                          "interface": interface[i],
                      },
                      "time": timestamp,
                      "fields": {
                          "current" : current,
                      }
                  }
                ]
                # Send the JSON data to InfluxDB
                influxclient.write_points(data)
            print('---')
    
            # Wait until it's time to query again...
            time.sleep(int(loop["interval"]))
     
    except KeyboardInterrupt:
        pass
