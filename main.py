# **************************************
# Load necessary libraries
import machine
from machine import Pin
import network
import onewire
import ds18x20
import urequests
import time
import credentials
from credentials import *


# **************************************
# Create objects:
led = machine.Pin(2,machine.Pin.OUT)
ds_pin =onewire.OneWire(Pin(4)) 
ds_sensor = ds18x20.DS18X20(ds_pin)
roms = ds_sensor.scan()

# **************************************
# Configure the ESP32 wifi as STAtion
sta = network.WLAN(network.STA_IF)

# Configure static IP
sta.ifconfig(['192.168.8.108', '255.255.255.0', '192.168.8.1', '192.168.8.1'])

if not sta.isconnected():
    print('connecting to network...')
    sta.active(True)

# sta.connect('your wifi ssid', 'your wifi password')
    sta.connect(ssid, password)
    while not sta.isconnected():
        pass
print('network config:', sta.ifconfig())


# **************************************
# Constants and variables:
HTTP_HEADERS = {'Content-Type': 'application/json'}

# initially there would be some delays
# before submitting the first update
# but should be enough to stabilize the
# the DS/DHT sensor.


def request(ds_readings):
    request = urequests.post(
      'http://api.thingspeak.com/update?api_key=' +
      thing_api,
      json=ds_readings,
      headers=HTTP_HEADERS)
    request.close()
    
# **************************************
# Main loop:
while True:
    led.off() # led off will turn led on (Board bug)
    
    ds_sensor.convert_temp()
    time.sleep_ms(3000)
    
    for rom in roms:
     print("read")
     time.sleep_ms(2000)
    temp = ds_sensor.read_temp(rom)
    ds_readings = {'field1': temp}

    if temp >= 30:
        request(ds_readings)  
        print("sending to server")
    print(temp)
    led.on() #led on will turn off led
    time.sleep_ms(115000)
