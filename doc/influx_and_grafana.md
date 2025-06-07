

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