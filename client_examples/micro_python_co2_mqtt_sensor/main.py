# Complete project details at https://RandomNerdTutorials.com
import time
import machine
import dht
from umqttsimple import MQTTClient
from MHZ19BSensor import MHZ19BSensor
from machine import Pin, I2C
#import ssd1306

d = dht.DHT11(machine.Pin(3))
co2_sensor = MHZ19BSensor(4, 5)
#i2c = I2C(1, sda=Pin(6), scl=Pin(7))
#display = ssd1306.SSD1306_I2C(128, 32, i2c)

def connect():
    global client_id, mqtt_server
    client = MQTTClient(client_id, mqtt_server)
    client.connect()
    print('Connected to %s MQTT broker' % (mqtt_server))
    return client

def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()

seconds = 120
while seconds >= 0:  # corrected the syntax error here
    print('Preheating co2 Sensor: %d' % seconds)
    seconds -= 1  # corrected the syntax error here
    time.sleep(1)

try:
    client = connect()
except OSError as e:
    restart_and_reconnect()

currentTime = time.ticks_ms()
while True:
    try:
        if time.ticks_ms() >= currentTime + 30000:
            d.measure()
            hRaw = d.humidity()
            tRaw = d.temperature()
            ppmRaw = co2_sensor.measure()            

            msg = b'{"temp": %d}' % (tRaw)
            client.publish(topic_pub, msg)
            print('Published: %s' % msg)
            msg = b'{"humidity": %d}' % (hRaw)
            client.publish(topic_pub, msg)
            print('Published: %s' % msg)
            msg = b'{"co2_ppm": %d}' % (ppmRaw)
            client.publish(topic_pub, msg)
            print('Published: %s' % msg)
            currentTime = time.ticks_ms()
            
            #hRaw_str = 'Humidity: %d %%' % hRaw
            #tRaw_str = 'Temp: %d C' % tRaw
            #ppmRaw_str = 'CO2: %d ppm' % ppmRaw

            #display.fill(0)
            #display.text(hRaw_str, 2, 0, 1)
            #display.text(tRaw_str, 2, 12, 1)
            #display.text(ppmRaw_str, 2, 24, 1)
            #display.show()

    except OSError as e:
        restart_and_reconnect()