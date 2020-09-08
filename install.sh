#!/bin/bash
apt-get update
apt-get upgrade
apt-get install python3 python3-pip python3-pymodbus python3-influxdb

cp ./dc_powermeter.py /usr/bin/
cp ./dc_powermeter.conf /etc/
cp ./dc_powermeter.service /lib/systemd/system/

systemctl daemon-reload
systemctl start dc_powermeter.service
systemctl enable dc_powermeter.service

#systemctl status dc_powermeter.service
