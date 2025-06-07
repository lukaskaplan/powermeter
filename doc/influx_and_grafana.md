
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

Example of docker-compose.yml for InfluxDB and Grafana:

```yml
services:
  influx:
    image: influxdb:1.8
    restart: always
    volumes:
      - influxdb:/var/lib/influxdb
    ports:
      - 8086:8086
    environment:
      INFLUXDB_DB: powermeter
      INFLUXDB_HTTP_AUTH_ENABLED: 'True'
      INFLUXDB_ADMIN_USER: admin
      INFLUXDB_ADMIN_PASSWORD: admin
      INFLUXDB_USER: user
      INFLUXDB_USER_PASSWORD: user
  
  grafana:
    image: grafana/grafana
    restart: always
    ports:
      - 3000:3000
```


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


