# powermeter

This project is cheap solution for measuring of AC current on up to 16 phases. It is based on chinese device labeled "HDHK", which has 16 inputs for measuring transformers.

This Device is powered by 12V DC power supply. Data are read via RS485 bus (modbus-rtu) which is connected to PC by RS485/USB converter. On the computer, there is running debian 10 with simple python script. Python script reds data from "HDHK" and sends them to remote InfluxDB. Then we can visualise them by Grafana.

![hdhk - chinese rs485 ampermeter](https://github.com/lukaskaplan/powermeter/blob/master/images/HDHK.jpg) 

# Connection diagram
![Connection diagram](https://github.com/lukaskaplan/powermeter/blob/master/powermeter.svg)




















# How to install it as a service
You will need linux server with usb port

```
apt update && apt install git
mkdir powermeter
cd powermeter
git clone https://github.com/lukaskaplan/powermeter
cd powermeter
chmod a+x ./install.sh
sudo ./install.sh

sudo systemctl status powermeter.service
```
# Option 1) Use it as zabbix_agent script
In this case you don't want to run it as a service and there will not be needed influx and grafana.
After instalation, stop and disable the powermeter service:

```
sudo systemctl stop powermeter.service
sudo systemctl disable powermeter.service
``` 

Ensure that service is stopped and disabled:

```
sudo systemctl status powermeter.service
```

Copy zabbix_agent config and reload zabbix_agent:

```
sudo cp ./zabbix_agentd.conf.d/userparameter-powermetter.conf /etc/zabbix/zabbix_agentd.conf.d/
sudo systemctl restart zabbix-agent.service
```

Test zabbix_agent userparameter:

```
$ sudo zabbix_agentd -t powermeter.current[a]
powermeter.current[a]                      [t|0.17]

$ sudo zabbix_agentd -t powermeter.current[b]
powermeter.current[b]                      [t|0.16]

$ sudo zabbix_agentd -t powermeter.current[c]
powermeter.current[c]                      [t|0.0]

```
### Zabbix item configuration:

 - Name: powermeter_current_A
 - Type: Zabbix agent
 - Key: powermeter.current[a]
 - Host interface: <IP address of your host>
 - Type: Numeric(float)
 - Units: A


  
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
  
# Option 3) How to run Influx and Grafana
In this case we want to run powermeter as a service, see section "How to install it as a service" above.

You will need running docker environment

```
mkdir /srv/powermeter
cd /srv/powermeter
git clone https://github.com/lukaskaplan/powermeter
cd powermeter
docker-compose up -d
```

### Test Influxdb:

**http://<yourserver_ip>:8086/query**

Cancel authentication and then you should get `"unable to parse authentication credentials"`. Or you can add credentials and after successful login, you shoud get `"missing required parameter \"q\""`


### Test Grafana:

**http://<yourserver_ip>:3000**

You should see login page. Default username and password is admin / admin.

Then you can import dashboards from this repo. You can see them below:

![Grafana owerview dashboard screenshot](https://github.com/lukaskaplan/powermeter/blob/master/images/screenshot1.png)

![Grafana history dashboard screenshot](https://github.com/lukaskaplan/powermeter/blob/master/images/screenshot2.png)



