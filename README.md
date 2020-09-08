# DC_powermeter

This project is cheap solution for measuring of AC current on up to 16 phases. It is based on cheap chinese device labeled "HDHK", which has 16 inputs for measuring transformers.

This Device is powered by 12V DC power supply. Data are read via RS485 bus (modbus-rtu) which can is connected to PC by RS485/USB converter. On the computer, there is running debian 10 with simple python script. Python script reds data from "HDHK" and sends them to remote InfluxDB. Then we can visualise them by Grafana.


![img](https://github.com/lukaskaplan/DC_powermeter/blob/master/images/HDHK.jpg) 
