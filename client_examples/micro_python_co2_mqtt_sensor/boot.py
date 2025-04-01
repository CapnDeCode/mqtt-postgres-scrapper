# Complete project details at https://RandomNerdTutorials.com

import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import webrepl

webrepl.start()

import gc
gc.collect()

ssid = 'SSID'
password = 'PASSWORD'
mqtt_server = '192.168.10.254'

client_id = b'pico_co2_sensor_2'
topic_pub = b'pico_co2_sensor_2'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while not station.isconnected():
    pass

print('Connection successful')
print(station.ifconfig())
