# MQTT Server with tls-ssl

TODO:

* Add config instructions for clients.
* Add subscriber python code example.
* Turn all command into `.env` variables and turn all command into a shell.
* Dockerize the broker?

## Steps

### 1. CA Private Key and Certificate

```sh
sudo openssl genrsa -out ca.key 2048
sudo openssl req -x509 -new -nodes -key ca.key -sha256 -days 365 -out ca.crt -subj "/C=VN/ST=Hanoi/L=Hanoi/O=ARIES/CN=MyCA"
```

### 2. Server Private Key and Certificate Signing Request

```sh
sudo openssl genrsa -out server.key 2048
sudo openssl req -new -key server.key -out server.csr -subj "/C=VN/ST=State/L=City/O=Organization/CN=your.server.domain"
```

To setup MQTT server for local area network, I can replace `your.server.domain` with `192.168.73.xxx`.

**Note**: Make sure the `-subj` of server key is different from the `-subj` of the CA certificates. Else, the "self-certificate" error will occur.

### 3. Sign the Server CSR with the CA Certificate

```sh
sudo openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365 -sha256
```

### 4. Verify config

```sh
sudo openssl verify -CAfile ca.crt server.crt
```

### 5. Copy/move files to designated place

Copy (keep original files in place):

```sh
sudo cp ca.* /etc/mosquitto/ca_certificates
sudo cp server.* /etc/mosquitto/certs
```

### 6. Modify file permissions

```sh
sudo chown mosquitto:mosquitto /etc/mosquitto/ca_certificates/ca.crt /etc/mosquitto/certs/server.crt /etc/mosquitto/certs/server.key
sudo chmod 640 /etc/mosquitto/ca_certificates/ca.crt /etc/mosquitto/certs/server.crt /etc/mosquitto/certs/server.key
```

### 7. Update Configuration

Configuration dir: `/etc/mosquitto/mosquitto.conf`.

```txt
listener 8883
cafile /etc/mosquitto/ca.crt
certfile /etc/mosquitto/server.crt
keyfile /etc/mosquitto/server.key
require_certificate true
tls_version tlsv1.2
```

### 8. Test configuration

```sh
mosquitto -c /etc/mosquitto/mosquitto.conf -v
```

### 9. Check log for error

```sh
sudo cat /var/log/mosquitto/mosquitto.log
```

### 10. (Optional) Send `ca.crt` to devices using `scp`

```sh
sudo scp /etc/mosquitto/ca_certificates/ca.crt user@remote_host:/home/user/
```

## [Sample Configs](./mosquitto.conf)

## Testing scripts on Python

* [publisher.py](./publisher.py).
* [subscriber.py](.)

## Common Errors

* `chmod` and `chown`: See step 6.
* `self-certification` error: See **Note** of step 2.
