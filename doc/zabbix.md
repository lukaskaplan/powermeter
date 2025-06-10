# Zabbix Integration Guide




 # Option 2) Use it as zabbix_agent script with json
 
Copy zabbix_agent config and reload zabbix_agent:

```
sudo cp ./zabbix_agentd.conf.d/userparameter-powermetter.conf /etc/zabbix/zabbix_agentd.conf.d/
sudo systemctl restart zabbix-agent.service
```

Test zabbix_agent userparameter:

```
sudo zabbix_agentd -t powermeter.json[/etc/powermeter/powermetter1.conf]

powermeter.json[/etc/powermeter/powermeter1.conf] [t|{"a": 3.51, "b": 3.77, "c": 1.3, "d": 3.51, "e": 3.88, "f": 1.97, "g": 1.23, "h": 0.0, "i": 1.55, "j": 1.55, "k": 2.02, "l": 4.0, "m": 0.47, "n": 0.0, "o": 4.91, "p": 0.0}]
```
### Zabbix item configuration (in template):

 - Name: powermeter
 - Type: Zabbix agent
 - Key: powermeter.json[{$PATH}]
 - Type of information: Text
  
### Zabbix dependent item (in template):

Item:
  - Name: Circuit 1
  - Type: Dependent item
  - Key: 1a
  - Master item: Template powermeter: powermeter
  - Type of information: Nuimeric (float)
  - Units: A
  
Preprocesing:
  - Name: JSONPath
  - Parameters: $.a
 
 ### Zabbix Host Macros
 Macro:
  - Macro: {$PATH}
  - Value: /etc/powermeter/powermeter1.conf
  - Description: Path to powermeter config file 



## How to test it

```bash
python3 scripts/powermeter_json.py config/powermeter/powermeter.json 2>&1

[Errno 2] could not open port /dev/ttyUSB1: [Errno 2] No such file or directory: '/dev/ttyUSB1'
WARNING:root:Device ID 2 on port /dev/ttyUSB1 - connection failed!
[
    {
        "id": 0,
        "device_id": 1,
        "input": "a",
        "name": "Input a",
        "current": 0.92
    },
    {
        "id": 1,
        "device_id": 1,
        "input": "b",
        "name": "Input b",
        "current": 0.14
    },
    {
        "id": 2,
        "device_id": 1,
        "input": "c",
        "name": "Input c",
        "current": 0.28
    },
    {
        "id": 3,
        "device_id": 1,
        "input": "d",
        "name": "Input d",
        "current": 0.0
    },
    {
        "id": 4,
        "device_id": 1,
        "input": "e",
        "name": "Input e",
        "current": 0.0
    },
    {
        "id": 5,
        "device_id": 1,
        "input": "f",
        "name": "Input f",
        "current": 0.0
    },
    {
        "id": 6,
        "device_id": 1,
        "input": "g",
        "name": "Input g",
        "current": 0.0
    },
    {
        "id": 7,
        "device_id": 1,
        "input": "h",
        "name": "Input h",
        "current": 0.0
    },
    {
        "id": 8,
        "device_id": 1,
        "input": "i",
        "name": "Input i",
        "current": 0.46
    },
    {
        "id": 9,
        "device_id": 1,
        "input": "j",
        "name": "Input j",
        "current": 0.0
    },
    {
        "id": 10,
        "device_id": 1,
        "input": "k",
        "name": "Input k",
        "current": 0.0
    },
    {
        "id": 11,
        "device_id": 1,
        "input": "l",
        "name": "Input l",
        "current": 0.0
    },
    {
        "id": 12,
        "device_id": 1,
        "input": "m",
        "name": "Input m",
        "current": 0.21
    },
    {
        "id": 13,
        "device_id": 1,
        "input": "n",
        "name": "Input n",
        "current": 0.0
    },
    {
        "id": 14,
        "device_id": 1,
        "input": "o",
        "name": "Input o",
        "current": 0.0
    },
    {
        "id": 15,
        "device_id": 1,
        "input": "p",
        "name": "Input p",
        "current": 0.0
    }
]

```