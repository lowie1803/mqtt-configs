# mqtt-configs

## Simple setups

### Clients

Use for simple MQTT interaction bash command, such as `mosquitto_sub` and `mosquitto_pub`.

```sh
sudo apt update
sudo apt install mosquitto-clients
```

Examples:

```sh
mosquitto_sub -h broker_address -t "device/test" -u "device_user" -P "password"

mosquitto_pub -h broker_address -t "device/test" -m "Hello World" -u "username" -P "password"
```

### Server

Use for broker server.

```sh
sudo apt-get update
sudo apt-get install mosquitto
```

Config the server at:

```txt
/etc/mosquitto/mosquitto.conf
```

***Sample configs for respective usage is in the subfolders of this repository.***
