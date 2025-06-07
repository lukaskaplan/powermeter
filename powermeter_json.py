################################################################
##                                                            ##
##                     Powermeter_json                        ##
##                                                            ##
## Description:                                               ##
##     This simple script reads current values                ##
##     from Chinese HDHK current meter via RS485 ModBUS-RTU   ##
##     and then returns data as JSON                          ##
##                                                            ##
## Author: Lukas Kaplan                                       ##
## Email: lukas.kaplan@lkaplan.cz                             ##
## License: BSD                                               ##
## Version: 1.1                                               ##
################################################################

import json
import sys
import os.path

from pymodbus.client import ModbusSerialClient as ModbusClient
from configparser import ConfigParser
  
### Read the config file ###
config_object = ConfigParser()

if len(sys.argv) > 1:
    if os.path.isfile(sys.argv[1]):
        ### Config file as argument
        config_object.read(sys.argv[1])
        
        modbus = config_object["modbus"]
        ratio = config_object["ratio"]
        
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
        connection = modbusclient.connect()
        
        request = modbusclient.read_holding_registers(address=8,count=16,slave=1)
        
        modbusclient.close()
        
        if connection:
            value = []
            current = float()
            for i in range(0,len(interface)):
                #current = float(ratio[interface[i]]) * float(request.registers[8+i])
                current = float(ratio[interface[i]]) * float(request.registers[i])
                current = round(current, 2)
                value.append(current)
        
            #print("Interface ",type(ratio[interface[i]]))
            #print("req",type(float(request.registers[8+i])))
            #print("current",type(current))
        
            output = dict(zip(interface,value))
            json = json.dumps(output,ensure_ascii = True)
            #json = json.dumps(output)
            print(json)
            #print(json.encode("ascii"))
        else:
            print('Connection lost, try again')
    else:
        print('Config file was not found:',sys.argv[1])
else:
    print('Missing argument - path to config file.')
