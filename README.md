# ⚡ Powermeter

**Powermeter** is a Python package for reading current values from **HDHK devices** (via RS-485 Modbus RTU) and exposing them in structured formats for monitoring and visualization.


## ✨ Features

- Reads Modbus RTU registers from HDHK devices
- Support for mutliple HDHK devices (each connected to the separated USB convertor)
- Provides easy-to-use API in Python (`get_values()`)
- Outputs JSON for use in Zabbix, InfluxDB, or other monitoring systems
- Can be run as a service or from CLI
- Easily extensible and modular


## 💡 Usage examples:

- **Datacenter** -> Monitor power consumption of per phase/fuse/circuit in an electrical switchboard. Use data for balance load, prevent overload, enable customer billing etc.
- **Home** -> Visualise home power consumption.
- **Camp** -> Measure power consumption on caravan sites.
- **Other** -> Use your imagination and needs.


## 🚀 Installation

### As Pyhon package (prefered way)

```bash
# Git clone
git clone https://github.com/lukaskaplan/powermeter.git
cd powermeter

# Create virtualenv
python3 -m venv /opt/powermeter-venv
source /opt/powermeter-venv/bin/activate

# Install
pip install -e .
```


### Configuration

```bash
# Copy config file
mkdir -p /etc/powermeter
cp config/powermeter/powermeter.json /etc/powermeter/

# Edit config file
nano /etc/powermeter/powermeter.json
```

## 🐍 Basic Usage (Python package)

Example usage in Python:

```python
from powermeter import get_values

values = get_values('/etc/powermeter/powermeter.json')
print(values)
```

Run your script:

```bash
/opt/powermeter-venv/bin/python3 <your-script>.py
```


## 📚 Further Documentation

- [Hardware installation guide](doc/hardware.md)
- [Zabbix integration guide](doc/zabbix.md)
- [InfluxDB + Grafana guide](doc/influx_and_grafana.md)


## 📄 License

This project is licensed under the MIT License. See LICENSE for details.


## 🤝 Contributing

Contributions are welcome! If you have suggestions, issues, or ideas, please open an issue or pull request.