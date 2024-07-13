import paho.mqtt.client as mqtt
import time

# MQTT broker details
broker_address = "192.168.1.100" 
broker_port = 8883
topic = "authorized/topic" # `username` must be authorized to access topic channel "authorized/*"
# This can be set in `acl config file`

# TLS/SSL certificates
ca_cert = "/home/pi/mqtt/ca.crt"
client_cert = "/home/pi/mqtt/client.crt"
client_key = "/home/pi/mqtt/client.key"

# Authentication details
username = "username"
password = "password"

# Create a new MQTT client instance
client = mqtt.Client()

# Configure TLS/SSL
client.tls_set(ca_certs=ca_cert, certfile=client_cert, keyfile=client_key)

# Set username and password
client.username_pw_set(username, password)

# Connect to the broker
client.connect(broker_address, broker_port)

# Example: Roll 2 dices each 30 seconds and publish the result on MQTT broker
import random
from datetime import datetime

def roll_dice(min=1, max=6):
  return random.randint(min, max)

def get_current_timestamp():
  return datetime.now().strftime("%b %d, %H:%M:%S")

# Publish messages to the topic
try:
  while True:
    dice1 = roll_dice()
    dice2 = roll_dice()
    msg = f"Timestamp: {get_current_timestamp()}. System has rolled 2 dices: {dice1} and {dice2}. Total: {dice1 + dice2}."
    client.publish(topic, msg)
    print(f"Published message: {msg} to topic: {topic}, on {broker_address}")
    time.sleep(30)  # Wait for 30 seconds before publishing the next message
except KeyboardInterrupt:
  print("Publishing stopped")
  client.disconnect()