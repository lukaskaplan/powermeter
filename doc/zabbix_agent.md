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
