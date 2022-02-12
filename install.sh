#!/bin/bash
apt-get update
apt-get upgrade
apt-get install python3 python3-pip python3-pymodbus python3-influxdb

cp ./powermeter.py /usr/local/bin/
cp ./powermeter.conf /etc/
cp ./powermeter.service /lib/systemd/system/

systemctl daemon-reload
systemctl start powermeter.service
systemctl enable powermeter.service

#systemctl status powermeter.service
