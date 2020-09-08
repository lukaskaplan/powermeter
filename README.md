# DC_powermeter

This project is cheap solution for measuring of AC current on up to 16 phases. It is based on cheap chinese device labeled "HDHK", which has 16 inputs for measuring transformers.

This Device is powered by 12V DC power supply. Data are read via RS485 bus (modbus-rtu) which can is connected to PC by RS485/USB converter. On the computer, there is running debian 10 with simple python script. Python script reds data from "HDHK" and sends them to remote InfluxDB. Then we can visualise them by Grafana.

![hdhk - chinese rs485 ampermeter](https://github.com/lukaskaplan/DC_powermeter/blob/master/images/HDHK.jpg) 

# Connection diagram
![Connection diagram](https://github.com/lukaskaplan/DC_powermeter/blob/master/DC_powermeter.svg)

# How to install python service
You will need linux server with usb port

```
mkdir dc_powermeter
cd dc_powermeter
git clone https://github.com/lukaskaplan/DC_powermeter
chmod a+x ./install.sh
sudo ./install.sh

systemctl status dc_powermeter.service
```

# How to run Influx and Grafana
You will need running docker environment

```
mkdir /srv/dc_powermeter
cd /srv/dc_powermeter
git clone https://github.com/lukaskaplan/DC_powermeter
docker-compose up -d
```

### Test Influxdb:

**http://<yourserver_ip>:8086/query**

Cancel authentication and then you should get `"unable to parse authentication credentials"`. Or you can add credentials and after successful login, you shoud get `"missing required parameter \"q\""`


### Test Grafana:

**http://<yourserver_ip>:3000**

You should see login page. Default username and password is admin / admin.

Then you can import dashboards from this repo. You can see them below:

![Grafana owerview dashboard screenshot](https://github.com/lukaskaplan/DC_powermeter/blob/master/images/screenshot1.png)

![Grafana history dashboard screenshot](https://github.com/lukaskaplan/DC_powermeter/blob/master/images/screenshot2.png)



